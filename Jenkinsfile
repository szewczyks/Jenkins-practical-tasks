pipeline {
    agent any
    options {
        skipDefaultCheckout(true)  // <--- disable auto checkout
    }
    environment {
        DOCKER_IMAGE = 'flask-ci-cd'
    }

    stages {
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
                sh 'git status'
            }
        }

        stage('Run Tests') {
            agent {
                docker {
                    image 'python:3.11'
                    args '-u root:root'
                }
            }
            steps {
                sh '''
                    python -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt pytest
                    ./venv/bin/pytest -q
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def tag = (env.BRANCH_NAME == 'main') ? 'latest' : env.BRANCH_NAME
                    sh """
                        docker build \
                          -t ${DOCKER_IMAGE}:${tag} \
                          -f docker/Dockerfile .
                    """
                }
            }
        }

        stage('Deploy (Local)') {
            when { branch 'main' }
            steps {
                sh '''
                    cd docker
                    docker compose down || true
                    docker compose up -d --build
                '''
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
