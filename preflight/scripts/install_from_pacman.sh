#!/usr/bin/env bash

sudo pacman -Syy
sudo pacman -S - < "$(pwd)/preflight/dependencies/preflight_pacman.txt"
