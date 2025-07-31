pipeline {
    agent any

    options {
        skipDefaultCheckout(true)        // blokujemy domyślne SCM
    }

    environment {
        DOCKER_IMAGE = 'flask-ci-cd'
    }

    stages {

        /* ---------- CHECKOUT & STASH ---------- */
        stage('Checkout') {
            steps {
                cleanWs()
                checkout scm
                sh 'git status -sb'
                // zapisz całe repo do stash'a o nazwie "src"
                stash name: 'src', includes: '**/*'
            }
        }

        /* ---------- TESTS in Python container ---------- */
        stage('Run Tests') {
            agent {
                docker {
                    image 'python:3.11'
                    args  '-u root:root'
                    reuseNode true              // użyj tego samego workspace
                }
            }
            steps {
                unstash 'src'                  // przywracamy kod w kontenerze
                sh '''
                    python -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt pytest
                    ./venv/bin/pytest -q
                '''
            }
        }

        /* ---------- BUILD Docker image ---------- */
        stage('Build Docker Image') {
            steps {
                unstash 'src'                  // na wszelki wypadek (gdyby workspace był pusty)
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

        /* ---------- DEPLOY locally ---------- */
        stage('Deploy (Local)') {
            when { branch 'main' }
            steps {
                sh '''
                    cd docker
                    docker-compose down || true
                    docker-compose up -d --build
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
