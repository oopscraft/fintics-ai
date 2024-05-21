pipeline {
    agent any
    parameters {
        string(name: 'IMAGE_NAMESPACE', defaultValue: params.IMAGE_NAMESPACE, description: 'image namespace')
        string(name: 'IMAGE_TAGS', defaultValue: params.IMAGE_TAGS, description: 'image tags')
        string(name:'IMAGE_REPO_URL', defaultValue: params.PUBLISHING_MAVEN_URL, description:'publishing maven url')
        credentials(credentialType: 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
                name: 'IMAGE_REPO_CREDENTIALS',
                defaultValue: params.IMAGE_REPO_CREDENTIALS,
                description: 'image repository credentials')
        string(name: 'SEND_MESSAGE_TO', defaultValue: params.SEND_MESSAGE_TO ?: '___', description: 'Message platform(SLACK|...)')
    }
    options {
        disableConcurrentBuilds()
    }
    stages {
        stage("prepare") {
            steps {
                cleanWs()
                checkout scm
            }
        }
        stage("build") {
            steps {
                sh '''
                docker build -t ${IMAGE_NAMESPACE}/fintics-ai:${IMAGE_TAGS} .
                '''.stripIndent()
            }
        }
        stage("publish") {
            environment {
                IMAGE_REPO_CREDENTIALS = credentials('IMAGE_REPO_CREDENTIALS')
            }
            steps {
                sh '''
                docker login 
                docker docker push ${IMAGE_NAMESPACE}/fintics-ai:${IMAGE_TAGS}
                '''.stripIndent()
            }
        }
        stage("deploy") {
            steps {
                sh '''
                    kubectl \
                    rollout restart deployment/fintics-ai \
                    -o yaml
                '''.stripIndent()
                sh '''
                    kubectl \
                    rollout status deployment/fintics-ai
                '''.stripIndent()
            }
        }
    }
    post {
        always {

            // junit
            junit allowEmptyResults: true, testResults: '**/build/test-results/test/*.xml'

            // send message
            script {
                if(params.SEND_MESSAGE_TO != null && params.SEND_MESSAGE_TO.contains('SLACK')) {
                    slackSend (
                        channel: '#oopscraftorg',
                        message: "Build [${currentBuild.currentResult}] ${env.JOB_NAME} (${env.BUILD_NUMBER}) - ${env.BUILD_URL}"
                    )
                }
            }
        }
    }

}