#!/usr/bin/env bash

sudo pacman -Syy
sudo pacman -S --needed - < "$(pwd)/preflight/dependencies/preflight_pacman.txt"
