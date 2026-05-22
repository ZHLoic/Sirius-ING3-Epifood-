set -euo pipefail
 
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
KUBELET="$SCRIPT_DIR/testHA.sh"
 
MASTER01="172.31.250.187"
MASTER02="172.31.250.115"
WORKER01="172.31.250.128"
WORKER02="172.31.250.154"
 
pause() {
  echo ""
  read -rp "  ↵  Appuyer sur ENTRÉE pour continuer..."
  echo ""
}
 

echo "kill master01 "
bash "$KUBELET" "$MASTER01" down
pause
 

echo "revive master01 ($MASTER01)"
bash "$KUBELET" "$MASTER01" up
pause

echo "kill worker01 "
bash "$KUBELET" "$WORKER01" down
pause
 

echo "revive worker01 ($WORKER01)"
bash "$KUBELET" "$WORKER01" up
pause

echo "fin demo"


sleep 3
echo "enfait non, on va faire un peu plus de dégâts"
echo "5"
sleep 1
echo "4"
sleep 1
echo "3"
sleep 1
echo "4"
sleep 1
echo "5"
sleep 1
timeout 5 curl ASCII.live/can-you-hear-me || true


echo "kill master02 + worker02 "
bash "$KUBELET" "$MASTER02" down
bash "$KUBELET" "$WORKER02" down
echo "killed"
pause
 

echo "revive master02 + worker02"
bash "$KUBELET" "$MASTER02" up
bash "$KUBELET" "$WORKER02" up
pause

echo "cette fois c'est fini"
curl parrot.live