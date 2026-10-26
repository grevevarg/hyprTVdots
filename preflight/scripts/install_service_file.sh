#!/usr/bin/env bash
set -euo pipefail

# user unit, so no sudo: a root-owned file in ~/.config breaks later edits
mkdir -p "$HOME/.config/systemd/user"
cp "$(pwd)/preflight/services/antimicrox-hyprdaemon.service" "$HOME/.config/systemd/user/antimicrox-hyprdaemon.service"
