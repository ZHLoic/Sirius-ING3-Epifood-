import paho.mqtt.client as mqtt
import json

# Configuration MQTT (VM2)
BROKER = "172.31.253.218"  # IP de la VM MQTT
PORT = 1883
TOPIC = "commandes"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

def envoyer_commande(commande):
    """
    Envoie une commande (ou recette) via MQTT
    """
    payload = json.dumps(commande)
    client.publish(TOPIC, payload)
    print(f"Commande envoyée via MQTT: {commande['_id']}")

