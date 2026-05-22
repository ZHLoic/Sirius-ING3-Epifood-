#!/usr/bin/env bash
# ============================================================
# Arrête ou démarre kubelet sur une machine distante via SSH
#
# Usage:
#   ./testHA <ip> <up|down>
#
# Exemples:
#   ./testHA 192.168.1.10 down   # arrête kubelet → machine "morte"
#   ./testHA 192.168.1.10 up     # démarre kubelet → machine "vivante"
# ============================================================

set -euo pipefail

# ── Aide ────────────────────────────────────────────────────
usage() {
  echo "Usage: $0 <ip> <up|down>"
  echo ""
  echo "  up    → démarre kubelet (machine accessible)"
  echo "  down  → arrête kubelet (simulation de mort)"
  exit 1
}

# ── Validation des arguments ─────────────────────────────────
[[ $# -lt 2 ]] && usage

TARGET_IP="$1"
USER="Adriend671"
SSH_TARGET="$USER@$TARGET_IP"
ACTION="$2"

case "$ACTION" in
  up|down) ;;
  *) echo "[ERREUR] Action invalide : '$ACTION'" && usage ;;
esac

# ── Exécution ─────────────────────────────────────────────────
echo ""
echo "═══════════════════════════════════════════"
if [[ "$ACTION" == "down" ]]; then
  echo " SIMULATION MORT ( C'est pour de faux hein ? ) → $TARGET_IP"
  ssh "$SSH_TARGET" "sudo systemctl stop kubelet && echo '[OK] kubelet arrêté'"
else
  echo " FIN SIMULATION MORT ( Pitié marche ) → $TARGET_IP"
  ssh "$SSH_TARGET" "sudo systemctl start kubelet && echo '[OK] kubelet démarré'"
fi
echo "═══════════════════════════════════════════"

echo ""
echo "[INFO] État de kubelet sur $TARGET_IP :"
ssh "$SSH_TARGET" "sudo systemctl status kubelet --no-pager | grep -E 'Active|Main PID'"
echo ""