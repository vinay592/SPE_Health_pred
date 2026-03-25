pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "vinayvb18/health-ml-app"
    }

    stages {

        stage('Clone Code') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $DOCKER_IMAGE .'
            }
        }

        stage('Push to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: '2e730b99-a7b8-40da-832b-cc55558031f1', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                        echo $PASS | docker login -u $USER --password-stdin
                        docker push $DOCKER_IMAGE
                    '''
                }
            }
        }

        stage('Deploy using Ansible') {
            steps {
                sh '''
                    cd ansible
                    ansible-playbook -i inventory.ini deploy.yml
                '''
            }
        }
    }

    post {
        success {
            echo 'Build + Deploy successful '
        }
        failure {
            echo 'Pipeline failed '
        }
    }
}
