pipeline {
    agent any
    
    environment {
        DOCKER_IMAGE = "taibaton/nnfs_pygamemysql"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    dockerImage = docker.build("${DOCKER_IMAGE}:${env.BUILD_ID}")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('', 'dockerhub-credentials-id') {
                        dockerImage.push('latest')
                        dockerImage.push("${env.BUILD_ID}")
                    }
                }
            }
        }
    }
}