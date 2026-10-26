#!/usr/bin/env bash
set -euo pipefail

# tee instead of >> so the write runs as root and re-runs replace the file instead of appending to it
sudo mkdir -p /etc/sddm.conf.d
sudo tee /etc/sddm.conf.d/autologin.conf > /dev/null << EOF2
[Autologin]
Session=hyprland
User=${SUDO_USER:-$(whoami)}
EOF2
