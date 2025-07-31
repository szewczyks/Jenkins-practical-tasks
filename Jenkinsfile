pipeline {
    agent {
        docker {
            image 'python:3.11'
            args '-u root:root'
        }
    }

    environment {
        VENV_DIR = 'venv'
        APP_NAME = 'flask-app'
        DOCKER_IMAGE = 'flask-ci-cd'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python') {
            steps {
                sh 'python3 -m venv ${VENV_DIR}'
                sh './${VENV_DIR}/bin/pip install --upgrade pip'
                sh './${VENV_DIR}/bin/pip install -r requirements.txt'
                sh './${VENV_DIR}/bin/pip install pytest'
            }
        }
        stage('Run Tests') {
            steps {
                sh './${VENV_DIR}/bin/pytest --maxfail=1 --disable-warnings -v'
            }
        }
        stage('Build Docker Image') {
            steps {
                script {
                    def tag = env.BRANCH_NAME == 'main' ? 'latest' : env.BRANCH_NAME
                    sh "docker build -t ${DOCKER_IMAGE}:${tag} -f docker/Dockerfile ."
                }
            }
        }
        stage('Deploy (Local)') {
            steps {
                script {
                    echo "Deploying branch ${env.BRANCH_NAME}..."
                    sh "cd docker && docker-compose down || true"
                    sh "cd docker && docker-compose up -d --build"
                }
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}