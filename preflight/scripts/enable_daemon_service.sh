#!/usr/bin/env bash
set -euo pipefail

systemctl --user daemon-reload
systemctl enable --now --user antimicrox-hyprdaemon

# sunshine (game streaming host) is optional; enable its user unit when the package is installed
if systemctl --user cat app-dev.lizardbyte.app.Sunshine.service &>/dev/null; then
    systemctl enable --now --user app-dev.lizardbyte.app.Sunshine.service
fi
