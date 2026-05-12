pipeline {
    agent any
    
    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'
        IMAGE_NAME = 'phirapong1125/it-repair-api'
        TAG = 'latest'
    }
    
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
        
        stage('Deploy Infrastructure (IaC)') {
            steps {
                script {
                    dir('terraform') {
                        sh 'terraform init'
                        sh 'terraform apply -auto-approve'
                    }
                    dir('ansible') {
                        // ใช้ catchError เพื่อไม่ให้ Pipeline ล้มเหลวถ้ารันเทสแล้วไม่มี Node จริง
                        catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE') {
                            sh 'ansible-playbook -i inventory playbook.yml'
                        }
                    }
                }
            }
        }
        
        stage('Deploy to Kubernetes') {
            steps {
                script {
                    sh 'kubectl apply -f k8s/deployment.yaml'
                    sh 'kubectl apply -f k8s/service.yaml'
                    sh 'kubectl rollout restart deployment/it-repair-api'
                }
            }
        }
        //
        stage('Deploy Monitoring Stack') {
            steps {
                script {
                    sh 'kubectl apply -f monitoring-stack.yaml'
                    sh 'kubectl rollout restart deployment/prometheus -n monitoring'
                    sh 'kubectl rollout restart deployment/grafana -n monitoring'
                }
            }
        }
    }
}