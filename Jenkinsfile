pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                script {
                    // Initial setup, installation of dependencies
                    sh 'make setup'
                }
            }
        }   

        stage('Unit Tests') {
            steps {
                script {
                    // Run unit tests and generate coverage report
                    sh 'make test'
                }
            }
        }

         stage('Statics Analysis ') {
            steps {
                script {
                    // Run unit tests and generate coverage report
                    sh 'make flake8'
                }
            }
        }

        stage('Generate Documentation') {
            steps {
                script {
                    // Generate documentation with pdoc
                    sh 'make docs'
                }
            }
        }

        stage('Coverage Checks') {
            steps {
                script {
                    // Check code coverage against a minimum threshold
                    sh 'make test-coverage'
                }
            }
        }
       
        
        stage('Deploy with Helmfile') {
            steps {
                echo 'deploy app'
            }
        }
    }

    post {
        always {
            // Archive generated reports for visualization in Jenkins
            archiveArtifacts artifacts: 'flake8_report.xml,coverage.xml,pytest.xml,docs/**', fingerprint: true
            testNG(showFailedBuilds: true, unstableFails: 5, unstableSkips: 25, failedFails:  10, failedSkips:   50)
    }
        }
    }
}
