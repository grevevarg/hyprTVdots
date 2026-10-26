#!/usr/bin/env bash
set -euo pipefail

yay -S --noconfirm - < "$(pwd)/preflight/dependencies/preflight_aur.txt"
