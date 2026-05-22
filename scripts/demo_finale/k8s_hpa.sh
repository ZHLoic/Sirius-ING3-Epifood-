#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <nombre_d_essai>"
    exit 1
fi

IP_MQTT="172.31.250.254"
RANGE=500

for i in $(seq 1 $1)
do
        CASINO=$(( RANDOM % RANGE + 1 ))
        echo CASINO:$CASINO
        mosquitto_pub -h $IP_MQTT -t lock/telemetry -m '{"badgeId":'$CASINO'}'
        echo "requete à:$IP_MQTT ID:$CASINO fait à $(date +"%H:%M:%S")" >> mock.log
done