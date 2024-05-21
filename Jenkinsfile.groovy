pipeline {
    agent any
    parameters {
        credentials(credentialType: 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
                name: 'JIB_FROM_AUTH_CREDENTIALS',
                defaultValue: params.JIB_FROM_AUTH_CREDENTIALS,
                description: 'base image repository credentials')
        string(name: 'JIB_TO_IMAGE_NAMESPACE', defaultValue: params.JIB_TO_IMAGE_NAMESPACE, description: 'target image')
        string(name: 'JIB_TO_TAGS', defaultValue: params.JIB_TO_TAGS, description: 'target image tags')
        credentials(credentialType: 'com.cloudbees.plugins.credentials.impl.UsernamePasswordCredentialsImpl',
                name: 'JIB_TO_AUTH_CREDENTIALS',
                defaultValue: params.JIB_TO_AUTH_CREDENTIALS,
                description: 'target image repository credentials')
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
            environment {
                MAVEN_CREDENTIALS = credentials('MAVEN_CREDENTIALS')
            }
            steps {
                sh '''
                docker build -t fintics-ai .
                '''.stripIndent()
            }
        }
        stage("publish") {
            environment {
                JIB_FROM_AUTH_CREDENTIALS = credentials('JIB_FROM_AUTH_CREDENTIALS')
                JIB_TO_AUTH_CREDENTIALS = credentials('JIB_TO_AUTH_CREDENTIALS')
            }
            steps {
                sh '''
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