# Workflow

## VM Setup
- Vault déjà setup sur la VM associée (initiée + ouverte) -> [epifood-vault]
- Secrets (Accès à la BD) déjà crées à l'intérieur -> [secret/data/epifood/db]
- Création d'une policy pour que le backend puisse uniquement lire les secrets de la BD -> [epifood-backend]
- Token d'accès renouvelable crée pour le backend

## Code
- Script permettant de récupérer les accès à la BD à partir du token -> [get_db_access.sh]
