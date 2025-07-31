pipeline {
    agent any

    environment {
        APP_NAME = 'flask-app'
    }

    stages {
        stage('Install dependecies') {
            steps {
                sh 'python -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
            }
        }
        stage('Run Tests') {
            steps {
                sh './vanv/bin/pytest --cov=app --cov-report=xml'
            }
        }
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $APP_NAME:${GIT_BRANCH}'
            }
        }
        stage('Deploy') {
            when {
                anyOf {
                    branch 'dev'
                    branch 'main'
                }
            }
            steps {
                script {
                    if (env.BRANCH_NAME == 'dev') {
                        sh './scripts/deploy_staging.sh'
                    } else if (env.BRANCH_NAME == 'main') {
                        sh '.scripts/deploy_prod.sh'
                    }
                }
            }
        }
    }
}