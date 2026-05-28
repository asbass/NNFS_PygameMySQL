pipeline {
    agent any
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t nnfs_pygamemysql:${env.BUILD_ID} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Dùng withCredentials để lấy user/pass từ Jenkins
                    withCredentials([usernamePassword(credentialsId: 'docker', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                        // BẮT BUỘC: Phải login trước khi push
                        sh "echo $PASS | docker login -u $USER --password-stdin"
                        
                        // Tag và Push
                        sh "docker tag nnfs_pygamemysql:${env.BUILD_ID} taibaton/nnfs_pygamemysql:latest"
                        sh "docker push taibaton/nnfs_pygamemysql:latest"
                    }
                }
            }
        }
    }
}
