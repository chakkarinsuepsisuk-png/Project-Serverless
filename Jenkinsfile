pipeline {
    agent any
    
    environment {
        // อ้างอิง ID ของ Credentials ที่ตั้งไว้ใน Jenkins
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'
        // !!! แก้ชื่อ username ด้านล่างนี้ !!!
        IMAGE_NAME = 'yaichakkarin/it-repair-api'
        TAG = 'latest'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                dir('app') {
                    script {
                        dockerImage = docker.build("${IMAGE_NAME}:${TAG}")
                    }
                }
            }
        }
        
        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('', DOCKERHUB_CREDENTIALS) {
                        dockerImage.push()
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                // สั่งรันอัปเดตลง Cluster
                sh 'kubectl apply -f k8s/deployment.yaml'
                sh 'kubectl apply -f k8s/service.yaml'
                // บังคับให้ดึง Image ตัวใหม่ไปรันเสมอ
                sh 'kubectl rollout restart deployment/it-repair-api'
            }
        }
    }
}