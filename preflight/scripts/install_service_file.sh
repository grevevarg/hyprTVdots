#!/usr/bin/env bash

sudo cp "$(pwd)/preflight/services/antimicrox-hyprdaemon.service" "/home/${SUDO_USER:-$(whoami)}/.config/systemd/user/antimicrox-hyprdaemon.service"
