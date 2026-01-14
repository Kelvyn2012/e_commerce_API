pipeline {
  agent any
  options { 
    timestamps()
    buildDiscarder(logRotator(numToKeepStr: '10')) // Keep last 10 builds
  }
  parameters {
    string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to build')
  }
  environment {
    GITHUB_CREDENTIALS_ID = 'github-creds'
    DOCKER_CREDENTIALS_ID = 'docker-hub-creds'
    IMAGE_NAME = 'kelvyn2012/e_commerce_api'
    REPORT_DIR = 'reports'
    PYTHON_VERSION = '3.10'
    DOCKER_IMAGE = "python:${PYTHON_VERSION}"
    // Add Git commit hash for better tracking
    GIT_COMMIT_SHORT = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()
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
      }
    }

    stage('Docker sanity check') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          sh 'docker version'
        }
      }
    }

    stage('Build Docker image') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          script {
            // Build with multiple tags for better tracking
            sh """
              docker build \
                --pull=false \
                --cache-from ${IMAGE_NAME}:latest \
                -t ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} \
                -t ${IMAGE_NAME}:${GIT_COMMIT_SHORT} \
                ${params.BRANCH == 'main' ? "-t ${IMAGE_NAME}:latest" : ""} \
                .
            """
          }
        }
      }
    }

    stage('Push Docker image') {
      when {
        expression { params.BRANCH == 'main' }
      }
      steps {
        withCredentials([usernamePassword(credentialsId: DOCKER_CREDENTIALS_ID, usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
          script {
            sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
            sh "docker push ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER}"
            sh "docker push ${IMAGE_NAME}:${GIT_COMMIT_SHORT}"
            sh "docker push ${IMAGE_NAME}:latest"
          }
        }
      }
    }

    stage('Run tests') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          script {
            // Remove || true to actually fail on test failures
            sh """
              docker run --rm \
                -v \$(pwd):/app \
                -w /app \
                ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} \
                sh -c 'pip install pytest pytest-cov && \
                       mkdir -p ${REPORT_DIR} && \
                       pytest --junitxml=${REPORT_DIR}/pytest-junit.xml \
                              --cov=. \
                              --cov-report=term-missing \
                              --cov-report=html:${REPORT_DIR}/coverage'
            """
          }
        }
      }
    }

    stage('Code Quality') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          script {
            // Keep || true here since pylint shouldn't fail the build
            sh """
              docker run --rm \
                -v \$(pwd):/app \
                -w /app \
                ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} \
                sh -c 'pip install pylint && \
                       pylint --output-format=parseable --reports=no **/*.py > ${REPORT_DIR}/pylint.log || true'
            """
          }
        }
      }
    }

    stage('Cleanup') {
      steps {
        script {
          // Clean up old build-tagged images (keep last 5)
          sh """
            # Get all build tags and sort them
            docker images ${IMAGE_NAME} --format '{{.Tag}}' | \
            grep -E '^${params.BRANCH}-[0-9]+\$' | \
            sort -t'-' -k2 -rn | \
            tail -n +6 | \
            xargs -r -I {} docker rmi ${IMAGE_NAME}:{} || true
            
            # Remove dangling images only
            docker image prune -f
          """
        }
      }
    }
  }
  
  post {
    always {
      junit allowEmptyResults: true, testResults: '**/reports/pytest-junit.xml'
      archiveArtifacts artifacts: '**/reports/**', allowEmptyArchive: true, fingerprint: true
      
      // Cleanup: logout from Docker Hub
      sh 'docker logout || true'
    }
    success {
      echo '✅ Pipeline succeeded!'
    }
    failure {
      echo '❌ Pipeline failed!'
      // Optionally notify team (Slack, email, etc.)
    }
    cleanup {
      // Clean workspace if needed
      cleanWs(deleteDirs: true, patterns: [[pattern: 'reports/**', type: 'INCLUDE']])
    }
  }
}