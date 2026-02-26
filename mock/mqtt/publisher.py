import paho.mqtt.client as mqtt
import json
from datetime import datetime

BROKER = "172.31.253.218"
PORT = 1883
TOPIC = "commandes"

# Création client MQTT global
client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[MQTT] Connecté au broker {BROKER}:{PORT}")
    else:
        print(f"[MQTT] Échec connexion MQTT, code {rc}")

client.on_connect = on_connect

# Connexion
try:
    client.connect(BROKER, PORT, 60)
    client.loop_start()  # loop MQTT en arrière-plan
except Exception as e:
    print(f"[MQTT] Impossible de se connecter : {e}")
    # Sérialisation datetime
def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def envoyer_commande(commande):
    """
    Envoie une commande via MQTT
    """
    global client

    # Assure que commande est un dict
    if isinstance(commande, tuple):
        keys = ['order_id', 'category', 'name', 'description', 'price',
                'start_order_time', 'prep_time', 'end_time_prep', 'status']
        commande = dict(zip(keys, commande))

    try:
        payload = json.dumps(commande, default=serialize_datetime)
        result = client.publish(TOPIC, payload)
        if result[0] == 0:
            print(f"[MQTT] Commande envoyée: {commande.get('order_id','UNKNOWN')}")
        else:
            print(f"[MQTT] Échec envoi commande: {commande.get('order_id','UNKNOWN')}")
    except Exception as e:
        print(f"[MQTT] Exception lors de l'envoi: {e}")
