# hyprTVdots
configuration for running hyprland on system plugged into tv
minimal version of the setup of my TV machine in https://github.com/grevevarg/homelab-state
for easier overview or for other people to borrow parts from it.
if you decide to install, note that there be dragons and that this is written for cachyOS. 
It should be easily migrateable to most systemd-based Arch distros.
As the name implies, this is for hyprland and if you want to use another DE you should probably only read through this project and borrow the parts relevant to you.

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

sets up automatic SDDM autologin
 - you are in control of not having any evil maids
 - follows worst security practices because i don't want to be bothered by a login screen when turning on my tv

 hypridle
  - set to suspend system after 1h of inactivity
  - in a perfect world waking on bluetooth should work but might need udev rules
  - see https://wiki.archlinux.org/title/Bluetooth#Wake_from_suspend

# generic controls
the antimicrox profile is written for an 8BitDo Ultimate 2C but should load for other controllers. I have no way to test.

reference controls under generic profile

`L1 (left shoulder button)` previous window
`R1 (right shoulder button)` next window
`GUIDE + d-pad up` increase volume
`GUIDE + d-pad down` decrease volume
`GUIDE + X` open application menu
`GUIDE + Y` toggle waybar
`GUIDE + right trigger` fullscreen
`GUIDE + left trigger` force close active window
`Left stick click` printscreen and save to ~/Pictures/screenshots/
`Right stick click` mouse right click
`A` mouse left click
`B` ESC
`d-pad up` keyboard up
`d-pad down` keyboard down
`d-pad left` keyboard left
`d-pad right` keyboard right

for controller profile media the only change is:
`A` enter

# note
webapps use global browser configuration and inherit extensions from them. its strongly suggested to install additional adblockers and some extension that lets you access youtube.com/tv

`installation`
if you're not ready to possibly get your hands dirty, you probably shouldn't.

clone repo
cd into repo
run `install.sh`
provide root password when prompted
