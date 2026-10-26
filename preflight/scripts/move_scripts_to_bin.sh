#!/usr/bin/env bash
set -euo pipefail

sudo cp "$(pwd)/bin/install-webapp" "/usr/local/bin/install-webapp"
sudo cp "$(pwd)/bin/antimicrox-hyprdaemon" "/usr/local/bin/antimicrox-hyprdaemon"
sudo cp "$(pwd)/bin/toggle_waybar" "/usr/local/bin/toggle_waybar"
