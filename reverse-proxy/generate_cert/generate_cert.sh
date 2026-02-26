#!/bin/bash

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <IP> <WEB_SERVER>"
    exit 1
fi

IP=$1
WEB_SERVER=$2

openssl req -x509 -nodes -days 365 \
-newkey rsa:2048 \
-keyout ../nginx/ssl/private/$WEB_SERVER.key \
-out ../nginx/ssl/certs/$WEB_SERVER.crt \
-subj "/CN=$IP"

echo key : ../nginx/ssl/private/$WEB_SERVER.key
echo cert: ../nginx/ssl/certs/$WEB_SERVER.crt