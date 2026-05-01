#!/usr/bin/env bash

# install dependencies
./preflight/scripts/install_from_pacman.sh
./preflight/scripts/install_yay.sh
./preflight/scripts/install_from_aur.sh
./preflight/scripts/install_flatpaks.sh
./preflight/scripts/install_webapps.sh
./preflight/scripts/move_scripts_to_bin.sh

# create default image folder structure + get wallpaper
./preflight/scripts/create_image_dirs.sh
./preflight/scripts/get_default_wallpaper.sh

# overwrite existing configs
./preflight/scripts/copy_configs.sh

# configure system
./preflight/scripts/install_service_file.sh
./preflight/scripts/sddm_autologin.sh
./preflight/scripts/enable_daemon_service.sh