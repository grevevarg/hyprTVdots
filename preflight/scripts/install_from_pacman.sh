#!/usr/bin/env bash
set -euo pipefail

sudo pacman -Syy
sudo pacman -S --needed - < "$(pwd)/preflight/dependencies/preflight_pacman.txt"
