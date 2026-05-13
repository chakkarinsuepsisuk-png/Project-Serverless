pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-credentials'
        IMAGE_NAME = 'yaichakkarin/it-repair-api'
        TAG = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Application') {

            agent {
                docker {
                    image 'python:3.9-slim'
                }
            }

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

                        def dockerImage = docker.build("${IMAGE_NAME}:${TAG}")

                        env.BUILT_IMAGE = "${IMAGE_NAME}:${TAG}"
                    }
                }
            }
        }

        stage('Push to Docker Hub') {

            steps {

                script {

                    docker.withRegistry('', DOCKERHUB_CREDENTIALS) {

                        sh "docker push ${env.BUILT_IMAGE}"

                    }
                }
            }
        }

        stage('Debug') {
            steps {
                withCredentials([file(credentialsId: 'gcp-service-account', variable: 'GOOGLE_CREDS')]) {
                    dir('terraform') {
                        sh '''
                        echo "CREDS FILE = $GOOGLE_CREDS"

                        cat $GOOGLE_CREDS | head

                        export GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_CREDS

                        gcloud auth activate-service-account --key-file=$GOOGLE_CREDS || true

                        gcloud auth list || true

                        '''
                    }
                }
            }
        }

        stage('Deploy Infrastructure (IaC)') {
            steps {

                withCredentials([
                    file(
                        credentialsId: 'gcp-service-account',
                        variable: 'GOOGLE_APPLICATION_CREDENTIALS'
                    )
                ]) {

                    dir('terraform') {

                        sh '''
                        echo "CREDS FILE = $GOOGLE_APPLICATION_CREDENTIALS"

                        terraform init
                        terraform apply -auto-approve
                        '''
                    }

                    dir('ansible') {

                        catchError(
                            buildResult: 'SUCCESS',
                            stageResult: 'FAILURE'
                        ) {

                            sh 'ansible-playbook -i inventory playbook.yml'
                        }
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {

            steps {

                withCredentials([
                    file(
                        credentialsId: 'gcp-service-account',
                        variable: 'GOOGLE_APPLICATION_CREDENTIALS'
                    )
                ]) {

                    script {

                        sh '''
                        gcloud auth activate-service-account \
                          --key-file=$GOOGLE_APPLICATION_CREDENTIALS
                        '''
                        sh "gcloud config set project it-repair-b6643577"
                        sh '''
                        gcloud container clusters get-credentials my-cluster \
                          --zone asia-southeast1
                        '''

                        sh "sed -i 's|image: yaichakkarin/it-repair-api:.*|image: yaichakkarin/it-repair-api:${BUILD_NUMBER}|' k8s/deployment.yaml"

                        sh 'kubectl apply -f k8s/deployment.yaml'
                        sh 'kubectl apply -f k8s/service.yaml'

                        sh 'kubectl rollout status deployment/it-repair-api'
                    }
                }
            }
        }

        stage('Deploy Monitoring Stack') {

            steps {

                script {

                    sh 'kubectl apply -f monitoring-stack.yaml'

                    sh '''
                    kubectl rollout restart deployment/prometheus -n monitoring || true
                    '''

                    sh '''
                    kubectl rollout restart deployment/grafana -n monitoring || true
                    '''
                }
            }
        }
    }

    post {

        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}