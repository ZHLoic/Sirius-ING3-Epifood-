#!/bin/bash

PATRONICTL="patronictl -c /etc/patroni/patroni.yml"
PRIMARY="172.31.252.17"
REPLICA1="172.31.252.233"
REPLICA2="172.31.249.151"

echo "======================================"
echo "TEST 1 : Etat initial du cluster"
echo "======================================"
$PATRONICTL list
echo ""

echo "======================================"
echo "TEST 2 : Connexion à la base de données"
echo "======================================"
psql -U postgres -h $PRIMARY -c "SELECT version();" && echo "Connexion PRIMARY OK" || echo "Connexion PRIMARY FAILED"
echo ""

echo "======================================"
echo "TEST 3 : Ecriture sur le primary"
echo "======================================"
psql -U postgres -h $PRIMARY -c "CREATE TABLE IF NOT EXISTS test_ha (id SERIAL, message TEXT, created_at TIMESTAMP DEFAULT NOW());"
psql -U postgres -h $PRIMARY -c "INSERT INTO test_ha (message) VALUES ('test failover $(date)');"
echo "Ecriture OK"
echo ""

echo "======================================"
echo "TEST 4 : Lecture sur les replicas"
echo "======================================"
psql -U postgres -h $REPLICA1 -c "SELECT * FROM test_ha ORDER BY id DESC LIMIT 1;" && echo "Lecture REPLICA1 OK" || echo "Lecture REPLICA1 FAILED"
psql -U postgres -h $REPLICA2 -c "SELECT * FROM test_ha ORDER BY id DESC LIMIT 1;" && echo "Lecture REPLICA2 OK" || echo "Lecture REPLICA2 FAILED"
echo ""

echo "======================================"
echo "TEST 5 : Simulation failover (arret primary)"
echo "======================================"
echo "Arret de Patroni sur le primary ($PRIMARY)..."
ssh cluster@$PRIMARY "sudo systemctl stop patroni"
echo "Attente de 15 secondes pour l election..."
sleep 15

echo "Nouvel etat du cluster :"
$PATRONICTL list
echo ""

echo "======================================"
echo "TEST 6 : Ecriture sur le nouveau leader"
echo "======================================"
NEW_LEADER=$($PATRONICTL list | grep Leader | awk '{print $4}')
echo "Nouveau leader : $NEW_LEADER"
psql -U postgres -h $NEW_LEADER -c "INSERT INTO test_ha (message) VALUES ('apres failover $(date)');" && echo "Ecriture apres failover OK" || echo "Ecriture apres failover FAILED"
echo ""

echo "======================================"
echo "TEST 7 : Retour du primary"
echo "======================================"
echo "Redemarrage de Patroni sur $PRIMARY..."
ssh cluster@$PRIMARY "sudo systemctl start patroni"
sleep 20
$PATRONICTL list
echo ""

echo "======================================"
echo "TEST 8 : Verification des donnees"
echo "======================================"
psql -U postgres -h $NEW_LEADER -c "SELECT * FROM test_ha ORDER BY id;"
echo ""

echo "======================================"
echo "TESTS TERMINES"
echo "======================================"
