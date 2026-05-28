pipeline {
    agent any
    
    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    // Dùng lệnh sh trực tiếp để build, an toàn hơn và không phụ thuộc vào plugin Docker
                    sh "docker build -t nnfs-pygame-mysql:${env.BUILD_ID} ."
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Cần chạy lệnh login trước (Lưu ý: Bạn nên lưu credentials trong Jenkins)
                    // Hoặc đơn giản hơn là để lệnh docker login ở ngoài máy EC2
                    sh "docker tag nnfs-pygame-mysql:${env.BUILD_ID} taibaton/nnfs-pygame-mysql:latest"
                    sh "docker push taibaton/nnfs-pygame-mysql:latest"
                }
            }
        }
    }
}
