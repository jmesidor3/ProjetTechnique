Comment ça marche : Jaeger : les traces de votre application seront envoyées à OpenTelemetry Collector, qui les transmet à Jaeger pour visualisation. Vous pouvez accéder à Jaeger à l'adresse http://localhost:16686. 

Prometheus : les métriques de votre application seront exposées à l'adresse http://localhost:8000 et pourront être collectées par Prometheus. 

Fluentd : les journaux de Biblio, MySQL, Nginx et Redis seront transmis à Fluentd et enregistrés dans des fichiers journaux ou envoyés sur stdout.

Étapes pour intégrer Grafana : ajoutez Grafana au fichier docker-compose.yml et configurez-le pour utiliser Prometheus comme source de données pour les métriques et Jaeger pour les traces. Configurez Prometheus comme système de collecte de métriques pour l'application et Grafana. Mettez à jour la configuration de Fluentd pour enregistrer les journaux spécifiques au service pour une meilleure observabilité. Ajoutez des tableaux de bord Grafana préconfigurés pour la visualisation des métriques et des traces de l'application.

Configuration de Prometheus (prometheus.yml) Nous devons configurer Prometheus pour extraire les métriques de votre application Flask (exposée sur localhost:8000) et des services système comme MySQL, Redis et Fluentd.

Configuration d'OpenTelemetry Collector (otel-collector-config.yaml) Cette configuration permet à OpenTelemetry Collector de recevoir des traces et de les exporter vers Jaeger, tout en exportant également des métriques vers Prometheus.

Configuration de Fluentd (fluentd.conf) Pour collecter les journaux de tous les services dans Docker Compose et les transmettre à Grafana, configurez Fluentd avec des sources d'entrée et de sortie appropriées.

Configuration de Grafana Accès à Grafana : une fois Grafana en cours d'exécution, vous pouvez y accéder via http://localhost:3000 avec les informations de connexion par défaut :

Nom d'utilisateur : admin Mot de passe : admin Ajouter des sources de données :

Prometheus (pour les métriques) :

Accédez à Configuration > Sources de données et ajoutez une nouvelle source de données. Sélectionnez Prometheus. Définissez l'URL sur http://prometheus:9090. Cliquez sur Enregistrer et tester. Jaeger (pour les traces) :

Accédez à Configuration > Sources de données et ajoutez une nouvelle source de données. Sélectionnez Jaeger. Définissez l'URL sur http://jaeger:16686. Cliquez sur Enregistrer et tester. Importer des tableaux de bord :

Grafana propose des tableaux de bord prédéfinis pour Prometheus et Jaeger. Accédez à Créer > Importer et saisissez l'ID du tableau de bord à partir du référentiel public de Grafana : Prometheus Flask Metrics : utilisez l'ID de tableau de bord 1860 pour les applications Flask. Jaeger Traces Dashboard : utilisez l'ID de tableau de bord 13649 pour les visualisations de traces Jaeger.

Accès aux tableaux de bord Grafana : Tableau de bord des métriques :

Ouvrez Grafana à l'adresse http://localhost:3000. Accédez au tableau de bord des métriques Prometheus Flask ou à tout autre tableau de bord pour les métriques. Tableau de bord de suivi :

Vous pouvez afficher les traces Jaeger dans Grafana après avoir configuré la source de données Jaeger. Tableaux de bord personnalisés :

Vous pouvez créer des tableaux de bord personnalisés pour les mesures d'application Redis, MySQL et Flask en interrogeant Prometheus et en visualisant les données dans Grafana.

Test et surveillance : Prometheus collectera les mesures à partir de :

L'application Flask exposée à /metrics sur le port 8000. Les exportateurs de mesures MySQL et Redis. Jaeger visualisera les traces collectées via OpenTelemetry Collector.

Fluentd regroupera les journaux de tous les services et les stockera pour analyse.

Nous disposons désormais d'une pile d'observabilité complète avec Grafana pour les tableaux de bord, Prometheus pour les mesures, Jaeger pour les traces et Fluentd pour les journaux. Cette configuration vous offre une surveillance et une journalisation complètes pour votre application, permettant une visualisation en temps réel des mesures et des traces sur l'ensemble des services.


python3 -m venv .venv 
source ./.venv/bin/activate
pip3 install -r requirements.txt




thrift: JaegerExporter
opentelemetry. importer.prometheus PrometheusMetricReader

chercher Jaeger sur github



