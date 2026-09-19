pipeline {

    agent any

    options {
        skipDefaultCheckout(true)
        timestamps()
    }

    environment {
        PATH = "/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin"
        IMAGE_NAME = "ai-devops-demo:${BUILD_NUMBER}"
        CONTAINER_NAME = "ai-devops-test-${BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Environment Check') {
            steps {
                sh '''
                    echo "PATH=$PATH"

                    echo "Git:"
                    which git
                    git --version

                    echo "Python:"
                    which python3
                    python3 --version

                    echo "Docker:"
                    which docker
                    docker --version

                    echo "Docker daemon:"
                    docker info
                '''
            }
        }

        stage('Unit Tests') {
            steps {
                sh '''
                    set -o pipefail
                    python3 -m unittest discover -s tests -v 2>&1 | tee test-results.log
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    set -o pipefail
                    docker build -t "$IMAGE_NAME" . 2>&1 | tee docker-build.log
                '''
            }
        }

        stage('Container Health Check') {
            steps {
                sh '''
                    docker run -d \
                        --name "$CONTAINER_NAME" \
                        -p 8081:8080 \
                        "$IMAGE_NAME"

                    sleep 2

                    curl --fail http://localhost:8081/health
                '''
            }
        }
    }

    post {

        always {
            sh '''
                docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
		docker image rm -f "$IMAGE_NAME" 2>/dev/null || true
            '''

            archiveArtifacts artifacts: '*.log',
                             allowEmptyArchive: true
        }

        success {
            echo 'CI/CD PIPELINE COMPLETED SUCCESSFULLY'
        }

        failure {
            echo 'CI/CD PIPELINE FAILED'
	    echo 'Starting AI failure analysis...'
	    
            sh '''
		python3 ai_analyzer.py test-results.log \
     	            > ai-analysis.txt 2>&1 || true
            '''
	    
            archiveArtifacts artifacts: 'ai-analysis.txt',
                    	     allowEmptyArchive: true

    	    sh 'cat ai-analysis.txt'
	
        }
    }
}
