pipeline {

    agent any

    environment {

        IMAGE_NAME = "taibaton/nnfs_webgame"

    }

    stages {

        stage('Build Docker Image') {

            steps {

                script {

                    echo "Building Docker image..."

                    sh """
                    docker build \
                    -t ${IMAGE_NAME}:${BUILD_ID} \
                    -t ${IMAGE_NAME}:latest .
                    """

                }

            }

        }
        
        stage('Push Docker Image') {

            steps {

                script {

                    withCredentials([
                        usernamePassword(
                            credentialsId: 'docker',
                            usernameVariable: 'DOCKER_USER',
                            passwordVariable: 'DOCKER_PASS'
                        )
                    ]) {

                        echo "Login Docker Hub..."

                        sh """
                        echo \$DOCKER_PASS | docker login \
                        -u \$DOCKER_USER \
                        --password-stdin
                        """

                        echo "Push Docker images..."

                        sh """
                        docker push ${IMAGE_NAME}:${BUILD_ID}
                        docker push ${IMAGE_NAME}:latest
                        """

                    }

                }

            }

        }
        stage('Push to ECR') {
            environment {
                // Thay bằng URL ECR của bạn
                ECR_REGISTRY = "123456789012.dkr.ecr.ap-southeast-1.amazonaws.com"
                IMAGE_NAME = "nnfs_webgame"
            }
            steps {
                script {
                    echo "Logging into ECR..."
                    // Lệnh này dùng AWS CLI để login (yêu cầu máy chủ Jenkins đã cài AWS CLI)
                    sh "aws ecr get-login-password --region ap-southeast-1 | docker login --username AWS --password-stdin ${ECR_REGISTRY}"

                    echo "Tagging and Pushing image..."
                    sh """
                    docker tag ${IMAGE_NAME}:${BUILD_ID} ${ECR_REGISTRY}/${IMAGE_NAME}:${BUILD_ID}
                    docker tag ${IMAGE_NAME}:latest ${ECR_REGISTRY}/${IMAGE_NAME}:latest
                    
                    docker push ${ECR_REGISTRY}/${IMAGE_NAME}:${BUILD_ID}
                    docker push ${ECR_REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }

    }

    post {

        always {

            echo "Cleaning Docker images..."

            sh """
            docker rmi ${IMAGE_NAME}:${BUILD_ID} || true
            docker rmi ${IMAGE_NAME}:latest || true
            """

        }

        success {

            echo "Pipeline Success"

        }

        failure {

            echo "Pipeline Failed"

        }

    }

}
