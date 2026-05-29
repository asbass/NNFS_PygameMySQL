pipeline {
    agent any
    environment {
        // Tên repo khớp với repo bạn tạo trên AWS ECR
        ECR_REGISTRY = "891920435433.dkr.ecr.ap-southeast-1.amazonaws.com"
        IMAGE_NAME = "nnfs_pygame_mysql" 
        FULL_IMAGE = "${ECR_REGISTRY}/${IMAGE_NAME}"
    }
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${FULL_IMAGE}:${BUILD_ID}..."
                    sh "docker build -t ${FULL_IMAGE}:${BUILD_ID} -t ${FULL_IMAGE}:latest ."
                }
            }
        }
        stage('Push to ECR') {
            steps {
                script {
                    echo "Logging into ECR..."
                    sh "aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin ${ECR_REGISTRY}"
                    
                    echo "Pushing images to ECR..."
                    sh "docker push ${FULL_IMAGE}:${BUILD_ID}"
                    sh "docker push ${FULL_IMAGE}:latest"
                }
            }
        }
        stage('Deploy to EKS') {
            steps {
                script {
                    echo "Updating EKS deployment..."
                    
                    if (fileExists('k8s/app.yaml')) {
                        // Sửa file YAML để trỏ tới image mới vừa push
                        sh "sed -i 's|image: .*|image: ${FULL_IMAGE}:${BUILD_ID}|g' k8s/app.yaml"
                        
                        // Đảm bảo namespace 'app' tồn tại
                        sh "kubectl create namespace app --dry-run=client -o yaml | kubectl apply -f -"
                        
                        // Deploy app
                        sh "kubectl apply -f k8s/app.yaml --namespace=app"
                        
                        echo "Deployment thành công cho ${IMAGE_NAME}!"
                    } else {
                        error "Không tìm thấy file k8s/app.yaml!"
                    }
                }
            }
        }
    }
    post {
        always {
            echo "Dọn dẹp..."
            sh "docker rmi ${FULL_IMAGE}:${BUILD_ID} || true"
        }
    }
}
