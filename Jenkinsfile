pipeline {
    agent any
    environment {
        // Cấu hình duy nhất 1 lần
        ECR_REGISTRY = "123456789012.dkr.ecr.ap-southeast-1.amazonaws.com"
        IMAGE_NAME = "nnfs_webgame"
        FULL_IMAGE = "${ECR_REGISTRY}/${IMAGE_NAME}"
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    // Build trực tiếp với tag ECR
                    sh "docker build -t ${FULL_IMAGE}:${BUILD_ID} -t ${FULL_IMAGE}:latest ."
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    echo "Logging into ECR..."
                    sh "aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                    
                    echo "Pushing to ECR..."
                    sh "docker push ${FULL_IMAGE}:${BUILD_ID}"
                    sh "docker push ${FULL_IMAGE}:latest"
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    echo "Updating EKS..."
                    // Dùng sed thay thế image trong file app.yaml của bạn
                    sh "sed -i 's|image: .*|image: ${FULL_IMAGE}:${BUILD_ID}|g' cicd/k8s/app.yaml"
                    sh "kubectl apply -f cicd/k8s/app.yaml --namespace=app"
                }
            }
        }
    }
    post {
        always {
            echo "Cleaning Docker images..."
            sh "docker rmi ${FULL_IMAGE}:${BUILD_ID} || true"
            sh "docker rmi ${FULL_IMAGE}:latest || true"
        }
    }
}
