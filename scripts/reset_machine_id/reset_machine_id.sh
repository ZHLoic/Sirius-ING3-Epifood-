#!/bin/bash

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <USER> <HOST> <PASSWORD>"
    exit 1
fi

REMOTE_USER=$1
REMOTE_HOST=$2
REMOTE_PASSWORD=$3

echo "Lancement du reset machine-id sur $REMOTE_USER@$REMOTE_HOST ..."

ssh "$REMOTE_USER@$REMOTE_HOST" "bash -s" <<ENDSSH
echo "reset du machine-id"

echo "$REMOTE_PASSWORD" | sudo -S rm -f /etc/machine-id
echo "$REMOTE_PASSWORD" | sudo -S rm -f /var/lib/dbus/machine-id
echo "$REMOTE_PASSWORD" | sudo -S rm -f /var/lib/systemd/network/* 2>/dev/null

echo "$REMOTE_PASSWORD" | sudo -S systemd-machine-id-setup
cat /etc/machine-id

echo "$REMOTE_PASSWORD" | sudo -S dhclient -r
echo "$REMOTE_PASSWORD" | sudo -S rm -f /var/lib/dhcp/* 2>/dev/null

echo "reboot dans 5 secondes..."
nohup bash -c "echo \"$REMOTE_PASSWORD\" | sudo -S reboot" >/tmp/machine-reset.log 2>&1 &

ENDSSH

echo "Script terminé, la VM va redémarrer."
