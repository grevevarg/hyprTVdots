#!/usr/bin/env bash
set -euo pipefail

systemctl --user daemon-reload
systemctl enable --now --user antimicrox-hyprdaemon
