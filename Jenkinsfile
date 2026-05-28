pipeline {
    agent any
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Dùng lệnh sh trực tiếp để build, an toàn hơn và không phụ thuộc vào plugin Docker
                    sh "docker build -t nnfs_pygamemysql:${env.BUILD_ID} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Cần chạy lệnh login trước (Lưu ý: Bạn nên lưu credentials trong Jenkins)
                    // Hoặc đơn giản hơn là để lệnh docker login ở ngoài máy EC2
                    withCredentials([usernamePassword(credentialsId: 'docker', passwordVariable: 'PASS', usernameVariable: 'USER')]) {
                    sh "docker tag nnfs_pygamemysql:${env.BUILD_ID} taibaton/nnfs_pygamemysql:latest"
                    sh "docker push taibaton/nnfs_pygamemysql:latest"
                }
                }
            }
        }
    }
}
