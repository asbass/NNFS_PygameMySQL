pipeline {
    agent any
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    sh "docker build -t taibaton/nnfs_pygamemysql:${env.BUILD_ID} -t taibaton/nnfs_pygamemysql:latest ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                        echo "Logging into Docker Hub..."
                        sh "echo $PASS | docker login -u $USER --password-stdin"
                        
                        echo "Pushing image to Docker Hub..."
                        sh "docker push taibaton/nnfs_pygamemysql:${env.BUILD_ID}"
                        sh "docker push taibaton/nnfs_pygamemysql:latest"
                    }
                }
            }
        }
    }
    
    post {
        always {
            script {
                echo "Cleaning up local images to save space..."
                sh "docker rmi taibaton/nnfs_pygamemysql:${env.BUILD_ID} || true"
            }
        }
        success {
            echo "CI/CD Pipeline finished successfully!"
        }
        failure {
            echo "CI/CD Pipeline failed. Please check the logs."
        }
    }
}
