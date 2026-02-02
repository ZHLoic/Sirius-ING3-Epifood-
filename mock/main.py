from db.pg_connexion import get_connexion, recuperer_recettes
from mqtt.publisher import envoyer_commande
import time

def main():
    conn = get_connexion()
    try:
        recettes = recuperer_recettes(conn)
        if not recettes:
            print("Pas de recettes disponibles.")
            return

        index = 0  # pour parcourir la liste des recettes
        while True:
            recette = recettes[index]
            envoyer_commande(recette)
            print(f"Commande envoyée: {recette['_id']}")

            # Passer à la recette suivante
            index += 1
            if index >= len(recettes):
                index = 0  # recommence depuis le début si on arrive à la fin

            # Attendre 1 minute avant la prochaine commande
            time.sleep(60)

    finally:
        conn.close()

if __name__ == "__main__":
    main()

