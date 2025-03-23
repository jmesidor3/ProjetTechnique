pipeline {
    agent any

    stages {
        stage('Lancement du pipeline') {
            steps {
                script {
                    // Initial setup, installation of dependencies
                    sh 'make setup'
                }
            }
        }   

        stage('Stimuler le trafic') {
            steps {
                script {
                    // Initial setup, installation of dependencies
                    sh 'make trafic'
                }
            }
        }   

        stage('Extraction des logs') {
            steps {
                script {
                    // Run unit tests and generate coverage report
                    sh 'make extract'
                }
            }
        }

         stage('Traitement des logs ') {
            steps {
                script {
                    // Run unit tests and generate coverage report
                    sh 'make traitement'
                }
            }
        }

        stage('Encodage des variables') {
            steps {
                script {
                    // Generate documentation with pdoc
                    sh 'make encodage'
                }
            }
        }

        stage('Generation de sequences') {
            steps {
                script {
                    // Check code coverage against a minimum threshold
                    sh 'make generation'
                }
            }
        }
        stage('Entrainement d un modele') {
            steps {
                // Checkout du code depuis le référentiel Git
                  sh 'make training'
            }
        }
        
        stage('Evaluation d un modele') {
            steps {
                sh 'make evaluation'
            }
        }
    }

    
    }

