# Script permetant a backend de récupérer les accès à la base de données depuis Vault.

# Vault config (token backend)
export VAULT_ADDR="https://127.0.0.1:8200"
export VAULT_SKIP_VERIFY=true
export VAULT_TOKEN="s.XXXXXXXXXXXXXXXXXXXXXX"  # Remplacer par le token réel

# Extraire les informations de la BD depuis Vault
vault kv get -format=json secret/epifood/db | jq -r '
  .data.data |
  "DB_USER=\(.username)\nDB_PASSWORD=\(.password)\nDB_HOST=\(.host)\nDB_NAME=\(.database)"
'
# EN ATTENTE -> IPFIRE en P1