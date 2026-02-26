from db.pg_connexion import get_connexion, recuperer_recettes
from mqtt.publisher import envoyer_commande
import time

def main():
    conn = get_connexion()
    try:
        print("[DEBUG] Connexion PostgreSQL OK")
        recettes = recuperer_recettes(conn)
        print(f"[DEBUG] Recettes récupérées : {recettes}")

        if not recettes:
            print("[DEBUG] Pas de recettes disponibles.")
            return

        keys = ['order_id', 'category', 'name', 'description', 'price',
                'start_order_time', 'prep_time', 'end_time_prep', 'status']

        print("[DEBUG] Début de la boucle d'envoi des commandes")
        index = 0
        while True:
            recette = recettes[index]
            recette_dict = dict(zip(keys, recette))  # convert tuple → dict
            envoyer_commande(recette_dict)
            print(f"[DEBUG] Commande envoyée: {recette_dict.get('order_id','UNKNOWN')}")

            index += 1
            if index >= len(recettes):
                index = 0

            time.sleep(60)

    finally:
        conn.close()
        print("[DEBUG] Connexion PostgreSQL fermée")

if __name__ == "__main__":
    main()
