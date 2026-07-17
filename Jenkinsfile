pipeline {
    agent any

    environment {
        ECR_REGISTRY = "891920435433.dkr.ecr.ap-southeast-1.amazonaws.com"
        IMAGE_NAME = "de00175-app"
        FULL_IMAGE = "${ECR_REGISTRY}/${IMAGE_NAME}"
    }

    stages {

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "docker build -t ${FULL_IMAGE}:${BUILD_ID} -t ${FULL_IMAGE}:latest ."
                }
            }
        }

        stage('Trivy Security Scan') {
            steps {
                script {
                    echo "Scanning Docker image..."

                    sh """
                    trivy image \
                    --severity HIGH,CRITICAL \
                    --exit-code 1 \
                    ${FULL_IMAGE}:${BUILD_ID}
                    """
                }
            }
        }

        stage('Push to ECR') {
            steps {
                script {
                    sh "aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin ${ECR_REGISTRY}"

                    sh "docker push ${FULL_IMAGE}:${BUILD_ID}"
                    sh "docker push ${FULL_IMAGE}:latest"
                }
            }
        }

        stage('Deploy to EKS') {
            steps {
                script {
                    sh "aws eks update-kubeconfig --region ap-southeast-1 --name DE00175-eks"

                    sh "sed -i 's|image: .*|image: ${FULL_IMAGE}:${BUILD_ID}|g' k8s/app.yaml"

                    sh "kubectl apply -f k8s/app.yaml --namespace=app --validate=false"
                }
            }
        }

        stage('Verify Rollout') {
            steps {
                script {
                    try {

                        sh """
                        kubectl rollout status deployment/de00175-app \
                        -n app \
                        --timeout=180s
                        """

                    } catch(Exception e) {

                        echo "Deployment failed. Rolling back..."

                        sh """
                        kubectl rollout undo deployment/de00175-app \
                        -n app
                        """

                        throw e
                    }
                }
            }
        }
    }

    post {
        always {
            sh "docker rmi ${FULL_IMAGE}:${BUILD_ID} || true"
        }
    }
}
