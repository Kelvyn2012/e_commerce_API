pipeline {
  agent any

  options {
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10'))
  }

  parameters {
    string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
  }

  environment {
    GITHUB_CREDENTIALS_ID = 'github-creds'
    DOCKER_CREDENTIALS_ID = 'docker-hub-creds'

    IMAGE_NAME = 'kelvyn2012/e_commerce_api'
    REPORT_DIR = 'reports'
    
    // Render
    RENDER_DEPLOY_HOOK = credentials('render-deploy-hook')
    HEALTHCHECK_URL = 'https://e-commerce-api-e7k5.onrender.com/health'

    // Quality gates
    PYLINT_FAIL_SCORE = '7.5'
  }

  stages {

    stage('Checkout') {
      steps {
        checkout([
          $class: 'GitSCM',
          branches: [[name: "*/${params.BRANCH}"]],
          userRemoteConfigs: [[
            url: 'https://github.com/Kelvyn2012/e_commerce_API.git',
            credentialsId: GITHUB_CREDENTIALS_ID
          ]]
        ])

        script {
          env.GIT_COMMIT_SHORT = sh(
            script: "git rev-parse --short HEAD",
            returnStdout: true
          ).trim()
          echo "Git commit: ${env.GIT_COMMIT_SHORT}"
        }
      }
    }

    stage('Docker sanity check') {
      steps {
        sh 'docker version'
        sh 'docker info'
      }
    }

    stage('Build Docker image') {
      steps {
        script {
          // Added --no-cache to ensure we aren't using an old empty layer
          sh """
            docker build --no-cache \
              -t ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} \
              -t ${IMAGE_NAME}:${env.GIT_COMMIT_SHORT} \
              ${params.BRANCH == 'main' ? "-t ${IMAGE_NAME}:latest" : ""} \
              .
          """
        }
      }
    }

    stage('Run tests') {
      steps {
        // 1. Removed -v mount (uses code inside image)
        // 2. Added SECRET_KEY env var
        // 3. Added container name 'test-container' to copy reports out later
        sh """
          docker run --name test-container-${BUILD_NUMBER} \
            -e SECRET_KEY='django-insecure-test-key' \
            -e DEBUG=True \
            ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} \
            sh -c '
              pip install pytest pytest-cov &&
              mkdir -p ${REPORT_DIR} &&
              pytest \
                --junitxml=${REPORT_DIR}/pytest-junit.xml \
                --cov=. \
                --cov-report=term-missing
            '
        """
        
        // Extract the test report from the container back to Jenkins workspace
        sh "docker cp test-container-${BUILD_NUMBER}:/app/${REPORT_DIR} . || true"
        
        // Cleanup the container
        sh "docker rm test-container-${BUILD_NUMBER}"
      }
    }

    stage('Lint') {
      steps {
        sh """
          docker run --rm \
            -e SECRET_KEY='django-insecure-test-key' \
            ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} \
            sh -c '
              pip install pylint &&
              pylint **/*.py --fail-under=${PYLINT_FAIL_SCORE}
            '
        """
      }
    }

    stage('Push Docker image') {
      when {
        expression { params.BRANCH == 'main' }
      }
      steps {
        withCredentials([usernamePassword(
          credentialsId: DOCKER_CREDENTIALS_ID,
          usernameVariable: 'DOCKER_USERNAME',
          passwordVariable: 'DOCKER_PASSWORD'
        )]) {
          sh '''
            echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
            docker push ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER}
            docker push ${IMAGE_NAME}:${GIT_COMMIT_SHORT}
            docker push ${IMAGE_NAME}:latest
          '''
        }
      }
    }

    stage('Deploy to Render') {
      when {
        expression { params.BRANCH == 'main' }
      }
      steps {
        sh """
          curl -X POST \
            -H "Accept: application/json" \
            "${RENDER_DEPLOY_HOOK}"
        """
        echo "Waiting for deployment to propagate..."
        sleep 30
      }
    }

    stage('Health check') {
      when {
        expression { params.BRANCH == 'main' }
      }
      steps {
        retry(5) {
          sh """
            STATUS=\$(curl -s -o /dev/null -w "%{http_code}" ${HEALTHCHECK_URL})
            if [ "\$STATUS" -ne 200 ]; then
              echo "Health check failed with status \$STATUS"
              exit 1
            fi
          """
        }
      }
    }
  }

  post {
    always {
      junit allowEmptyResults: true, testResults: '**/reports/pytest-junit.xml'
      archiveArtifacts artifacts: '**/reports/**', allowEmptyArchive: true
      sh 'docker logout || true'
    }

    success {
      echo 'Pipeline succeeded'
    }

    failure {
      echo 'Pipeline failed'
    }

    cleanup {
      cleanWs(deleteDirs: true)
    }
  }
}