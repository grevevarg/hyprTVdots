#!/usr/bin/env bash
set -euo pipefail

# already installed on re-runs (and on cachyOS); the clone below would fail on an existing yay/ dir
if command -v yay > /dev/null; then
    exit 0
fi

prevdir="$(pwd)"

sudo pacman -S --needed git base-devel && git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si

cd "$prevdir"
