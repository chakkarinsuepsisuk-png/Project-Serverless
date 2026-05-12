pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Test Application') {
            steps {
                dir('app') {
                    sh 'python3 -m py_compile app.py'
                }
            }
        }
    }
}