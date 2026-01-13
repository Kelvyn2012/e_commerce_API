pipeline {
  agent any
  options { timestamps() }
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
            sh "docker build -t ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} ."
            
            if (params.BRANCH == 'main') {
              sh "docker tag ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} ${IMAGE_NAME}:latest"
            }
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
            sh "docker push ${IMAGE_NAME}:latest"
          }
        }
      }
    }

    stage('Run tests') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          script {
            sh """
              docker run --rm \
                -v \$(pwd):/app \
                -w /app \
                ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} \
                sh -c 'pip install pytest pytest-cov && mkdir -p ${REPORT_DIR} && pytest -q --junitxml=${REPORT_DIR}/pytest-junit.xml --cov=. --cov-report=term-missing || true'
            """
          }
        }
      }
    }

    stage('Code Quality') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          script {
            sh """
              docker run --rm \
                -v \$(pwd):/app \
                -w /app \
                ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} \
                sh -c 'pip install pylint && pylint --exit-zero **/*.py || true'
            """
          }
        }
      }
    }

    stage('Cleanup') {
      steps {
        script {
          sh 'docker image prune -f'
        }
      }
    }
  }
  
  post {
    always {
      junit allowEmptyResults: true, testResults: '**/reports/pytest-junit.xml'
      archiveArtifacts artifacts: '**/reports/**', allowEmptyArchive: true, fingerprint: true
    }
    success {
      echo '✅ Pipeline succeeded!'
    }
    failure {
      echo '❌ Pipeline failed!'
    }
  }
}