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
          // Get Git commit hash after checkout
          env.GIT_COMMIT_SHORT = sh(
            script: "git rev-parse --short HEAD",
            returnStdout: true
          ).trim()
          echo "📌 Git commit: ${env.GIT_COMMIT_SHORT}"
        }
      }
    }

    stage('Docker sanity check') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          sh 'docker version'
          sh 'docker info | grep -i "Docker Root Dir\\|Storage Driver"'
        }
      }
    }

    stage('Build Docker image') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          script {
            echo "🔨 Building Docker image..."
            
            // Build with multiple tags for better tracking
            def buildCommand = """
              docker build \
                --pull=false \
                --cache-from ${IMAGE_NAME}:latest \
                -t ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} \
                -t ${IMAGE_NAME}:${env.GIT_COMMIT_SHORT} \
                ${params.BRANCH == 'main' ? "-t ${IMAGE_NAME}:latest" : ""} \
                .
            """
            
            sh buildCommand
            
            echo "✅ Docker image built successfully"
            echo "📦 Tags created:"
            echo "   - ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER}"
            echo "   - ${IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"
            if (params.BRANCH == 'main') {
              echo "   - ${IMAGE_NAME}:latest"
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
        timeout(time: 10, unit: 'MINUTES') {
          withCredentials([usernamePassword(
            credentialsId: DOCKER_CREDENTIALS_ID, 
            usernameVariable: 'DOCKER_USERNAME', 
            passwordVariable: 'DOCKER_PASSWORD'
          )]) {
            script {
              // Login with exponential backoff retry
              def loginAttempts = 0
              def maxLoginAttempts = 3
              def loginSuccess = false
              
              while (loginAttempts < maxLoginAttempts && !loginSuccess) {
                try {
                  loginAttempts++
                  echo "🔑 Docker Hub login attempt ${loginAttempts}/${maxLoginAttempts}..."
                  
                  sh '''
                    set +x  # Hide password in logs
                    echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                    set -x
                  '''
                  
                  loginSuccess = true
                  echo "✅ Docker Hub login successful"
                  
                } catch (Exception e) {
                  if (loginAttempts >= maxLoginAttempts) {
                    error("❌ Failed to login to Docker Hub after ${maxLoginAttempts} attempts: ${e.message}")
                  }
                  def waitTime = loginAttempts * 5
                  echo "⚠️  Login failed: ${e.message}"
                  echo "⏳ Retrying in ${waitTime} seconds..."
                  sleep waitTime
                }
              }
              
              // Push build-specific tag
              echo "📤 Pushing ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER}..."
              retry(3) {
                sh "docker push ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER}"
              }
              echo "✅ Pushed build tag successfully"
              
              // Push git commit tag
              echo "📤 Pushing ${IMAGE_NAME}:${env.GIT_COMMIT_SHORT}..."
              retry(3) {
                sh "docker push ${IMAGE_NAME}:${env.GIT_COMMIT_SHORT}"
              }
              echo "✅ Pushed commit tag successfully"
              
              // Push latest tag
              echo "📤 Pushing ${IMAGE_NAME}:latest..."
              retry(3) {
                sh "docker push ${IMAGE_NAME}:latest"
              }
              echo "✅ Pushed latest tag successfully"
              
              echo "🎉 All images pushed to Docker Hub"
            }
          }
        }
      }
    }

    stage('Run tests') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          script {
            echo "🧪 Running tests..."
            
            try {
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
              echo "✅ Tests passed"
            } catch (Exception e) {
              echo "⚠️  Tests failed: ${e.message}"
              currentBuild.result = 'UNSTABLE'
              // Continue pipeline but mark as unstable
            }
          }
        }
      }
    }

    stage('Code Quality') {
      steps {
        wrap([$class: 'AnsiColorBuildWrapper', colorMapName: 'xterm']) {
          script {
            echo "📊 Running code quality checks..."
            
            // Keep || true here since pylint shouldn't fail the build
            sh """
              docker run --rm \
                -v \$(pwd):/app \
                -w /app \
                ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER} \
                sh -c 'pip install pylint && \
                       mkdir -p ${REPORT_DIR} && \
                       pylint --output-format=parseable --reports=no **/*.py > ${REPORT_DIR}/pylint.log || true'
            """
            
            echo "✅ Code quality check completed"
          }
        }
      }
    }

    stage('Cleanup') {
      steps {
        script {
          echo "🧹 Cleaning up old images..."
          
          // Clean up old build-tagged images (keep last 5)
          sh """
            echo "Checking for old build images to remove..."
            
            # Get all build tags and sort them
            OLD_IMAGES=\$(docker images ${IMAGE_NAME} --format '{{.Tag}}' | \
              grep -E '^${params.BRANCH}-[0-9]+\$' | \
              sort -t'-' -k2 -rn | \
              tail -n +6)
            
            if [ -n "\$OLD_IMAGES" ]; then
              echo "Removing old images: \$OLD_IMAGES"
              echo "\$OLD_IMAGES" | xargs -r -I {} docker rmi ${IMAGE_NAME}:{} || true
              echo "✅ Old images removed"
            else
              echo "ℹ️  No old images to remove"
            fi
            
            # Remove dangling images only
            echo "Removing dangling images..."
            docker image prune -f
            
            echo "✅ Cleanup completed"
          """
        }
      }
    }
  }
  
  post {
    always {
      script {
        echo "📋 Archiving test results and artifacts..."
      }
      
      junit allowEmptyResults: true, testResults: '**/reports/pytest-junit.xml'
      archiveArtifacts artifacts: '**/reports/**', allowEmptyArchive: true, fingerprint: true
      
      // Cleanup: logout from Docker Hub
      sh 'docker logout || true'
      
      script {
        // Display build summary
        echo """
        ═══════════════════════════════════════════════════════
        📊 BUILD SUMMARY
        ═══════════════════════════════════════════════════════
        Branch:        ${params.BRANCH}
        Build Number:  ${BUILD_NUMBER}
        Git Commit:    ${env.GIT_COMMIT_SHORT}
        Image Tags:    
          - ${IMAGE_NAME}:${params.BRANCH}-${BUILD_NUMBER}
          - ${IMAGE_NAME}:${env.GIT_COMMIT_SHORT}
          ${params.BRANCH == 'main' ? "- ${IMAGE_NAME}:latest" : ""}
        Result:        ${currentBuild.result ?: 'SUCCESS'}
        Duration:      ${currentBuild.durationString?.replace(' and counting', '')}
        ═══════════════════════════════════════════════════════
        """
      }
    }
    
    success {
      echo '✅ Pipeline succeeded!'
      // TODO: Add notification (Slack, email, etc.)
      // slackSend color: 'good', message: "Build ${BUILD_NUMBER} succeeded!"
    }
    
    unstable {
      echo '⚠️  Pipeline completed with warnings (tests may have failed)'
      // TODO: Add notification
    }
    
    failure {
      echo '❌ Pipeline failed!'
      // TODO: Add notification (Slack, email, etc.)
      // slackSend color: 'danger', message: "Build ${BUILD_NUMBER} failed!"
    }
    
    cleanup {
      // Clean workspace reports directory
      cleanWs(
        deleteDirs: true, 
        patterns: [
          [pattern: 'reports/**', type: 'INCLUDE']
        ],
        notFailBuild: true
      )
    }
  }
}