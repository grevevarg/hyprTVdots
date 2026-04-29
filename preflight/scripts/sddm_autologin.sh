#!/usr/bin/env bash

sudo mkdir -p /etc/sddm.conf.d
sudo cat << EOF >> /etc/sddm.conf.d/autologin.conf
[General]
Session=hyprland
User=${SUDO_USER:-$(whoami)}
EOF
