from confluent_kafka import Producer
import json
from datetime import datetime

BROKER = "172.31.249.46:9092"
TOPIC = "commandes"

producer = Producer({'bootstrap.servers': BROKER})

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")

def envoyer_commande(commande):
    if isinstance(commande, tuple):
        keys = ['order_id', 'category', 'name', 'description', 'price',
                'start_order_time', 'prep_time', 'end_time_prep', 'status']
        commande = dict(zip(keys, commande))

    try:
        payload = json.dumps(commande, default=serialize_datetime)
        producer.produce(TOPIC, payload.encode('utf-8'))
        producer.flush()
        print(f"[KAFKA] Commande envoyée: {commande.get('order_id', 'UNKNOWN')}")
    except Exception as e:
        print(f"[KAFKA] Exception lors de l'envoi: {e}")





