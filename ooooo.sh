#!/bin/bash

# URL du webhook Discord
WEBHOOK_URL="https://discord.com/api/webhooks/1313248626922881064/d68n1GxULvUiyTsRJ9AcdF8ocOnA7MaWlr7aCRq7sVqmGu_fHQqZDqZxhzLiM09QerAp"

# Générer des dates aléatoires
generate_random_date() {
    local random_date=$(date -d "$((RANDOM % 7)) days ago $((RANDOM % 24)) hours ago $((RANDOM % 60)) minutes ago $((RANDOM % 60)) seconds ago" +"%Y-%m-%d %H:%M:%S")
    echo "$random_date"
}

# Envoyer une alerte à Discord
send_alert_to_discord() {
    local alert_name=$1
    local alert_time=$2
    local alert_details=$3

    # Message à envoyer
    local message="Alert: $alert_name | Time: $alert_time | Details: $alert_details"

    # Envoyer via curl
    curl -X POST -H "Content-Type: application/json" -d "{\"content\": \"$message\"}" "$WEBHOOK_URL"
}

# Générer et envoyer des alertes MySQL et CPU
for i in {1..5}; do
    # Alertes MySQL
    alert_name="MySQL Down"
    alert_time=$(generate_random_date)
    alert_details="Randomly generated alert for MySQL Down."
    send_alert_to_discord "$alert_name" "$alert_time" "$alert_details"

    # Alertes CPU
    alert_name="High CPU Usage"
    alert_time=$(generate_random_date)
    alert_details="Randomly generated alert for High CPU Usage."
    send_alert_to_discord "$alert_name" "$alert_time" "$alert_details"
done

echo "All alerts have been sent to Discord."
