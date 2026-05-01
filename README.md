# hyprTVdots
configuration for running hyprland on system plugged into tv</br>
minimal version of the setup of my TV machine in https://github.com/grevevarg/homelab-state</br>
for easier overview or for other people to borrow parts from it.</br>
if you decide to install, note that there be dragons and that this is written for cachyOS. </br>
It should be easily migrateable to most systemd-based Arch distros.</br>
As the name implies, this is for hyprland and if you want to use another DE you should probably only read through this project and borrow the parts relevant to you.</br>

# features
controller centric navigation, using a daemon for swapping between profiles based on currently active window name
 - the default behaviour when a name isn't matched is to release controller binds entirely as its assumed that a game with controller support has been launched
 - if mouse controls are needed but the window defaulted to releasing controls, a keyboard is needed and you can use SUPER+SHIFT+S to load the generic config

toggleable vertical waybar that loads generic controller profile when launched and restores to previous when hidden

modules:
 - bluetooth
 - wifi
 - power menu
 - clock

sets up SDDM autologin
 - you are in control of not having any evil maids
 - follows worst security practices because i don't want to be bothered by a login screen when turning on my tv

 hypridle
  - set to suspend system after 1h of inactivity
  - in a perfect world waking on bluetooth should work but might need udev rules
  - see https://wiki.archlinux.org/title/Bluetooth#Wake_from_suspend

# generic controls
the antimicrox profile is written for an 8BitDo Ultimate 2C but should load for other controllers. I have no way to test.

reference controls under generic profile

`L1 (left shoulder button)` previous window</br>
`R1 (right shoulder button)` next window</br>
`GUIDE + d-pad up` increase volume</br>
`GUIDE + d-pad down` decrease volume</br>
`GUIDE + X` open application menu</br>
`GUIDE + Y` toggle waybar</br>
`GUIDE + right trigger` fullscreen</br>
`GUIDE + left trigger` force close active window</br>
`Left stick click` printscreen and save to ~/Pictures/screenshots/</br>
`Right stick click` mouse right click</br>
`A` mouse left click</br>
`B` ESC</br>
`d-pad up` keyboard up</br>
`d-pad down` keyboard down</br>
`d-pad left` keyboard left</br>
`d-pad right` keyboard right</br>

for controller profile media the only change is:</br>
`A` enter

# note
webapps use global browser configuration and inherit extensions from them. its strongly suggested to install additional adblockers and some extension that lets you access youtube.com/tv

# installation
if you're not ready to possibly get your hands dirty, you probably shouldn't.</br>
to discourage installing this willy nilly, no extremely detailed instructions are given.

clone repo</br>
cd into repo</br>
run `install.sh`</br>
provide root password when prompted</br>
