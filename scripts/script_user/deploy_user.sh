#!/bin/bash

# --- CONFIG LOCAL --------------------------------------------------------

# script permetant de créer un user avec les droits sudo et de deployer sa clé publique.

if [ $# -lt 3 ]; then
    echo "Usage: $0 <REMOTE_HOST> <REMOTE_USER>"
        exit 1
fi

CONFIG_FILE=config.conf
REMOTE_HOST="$1"
REMOTE_USER="$2"

source "$CONFIG_FILE"

if [ -z "$USERNAME" ] || [ -z "$PASSWORD" ] || [ -z "$SSH_KEY" ] || [ -z "$REMOTE_PASSWORD" ]; then
	    echo "Erreur : une ou plusieurs variables manquent dans $CONFIG_FILE"
	        exit 1
fi

echo "[INFO] Connexion à la VM distante : $REMOTE_HOST"
echo "[INFO] Création de l'utilisateur : $USERNAME"

# --- COMMANDES DISTANTES ---
sshpass -p "$REMOTE_PASSWORD" ssh -o StrictHostKeyChecking=no "$REMOTE_USER@$REMOTE_HOST" bash <<EOF

# 1. Créer l'utilisateur s'il n'existe pas
if ! id "$USERNAME" >/dev/null 2>&1; then
    echo "[VM] Création de l'utilisateur $USERNAME"
    echo "$REMOTE_PASSWORD" | sudo -S useradd -m -s /bin/bash "$USERNAME"
fi

# 2. Définir le mot de passe du nouvel utilisateur
echo "$REMOTE_PASSWORD" | sudo -S bash -c "echo '$USERNAME:$PASSWORD' | chpasswd"

# 3. Ajouter aux sudoers
echo "$REMOTE_PASSWORD" | sudo -S usermod -aG sudo "$USERNAME"

# 4. Configuration SSH
echo "$REMOTE_PASSWORD" | sudo -S mkdir -p /home/$USERNAME/.ssh
echo "$SSH_KEY" | sudo tee /home/$USERNAME/.ssh/authorized_keys >/dev/null
echo "$REMOTE_PASSWORD" | sudo -S chmod 700 /home/$USERNAME/.ssh
echo "$REMOTE_PASSWORD" | sudo -S chmod 600 /home/$USERNAME/.ssh/authorized_keys
echo "$REMOTE_PASSWORD" | sudo -S chown -R $USERNAME:$USERNAME /home/$USERNAME/.ssh

echo "[VM] Configuration terminée."
EOF

echo "[OK] Déploiement terminé."
