-- hyprland.start runs once at startup, not on reload.
-- exec_cmd runs `sh -c cmd`, so pipes/&&/$(...) work.

hl.on("hyprland.start", function()
    -- clipboard history, for script compatibility only (no bind or rofi entry)
    hl.exec_cmd("wl-paste --type text --watch cliphist store")
    hl.exec_cmd("wl-paste --type image --watch cliphist store")
    hl.exec_cmd("dbus-update-activation-environment --systemd WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
    hl.exec_cmd("systemctl --user import-environment WAYLAND_DISPLAY XDG_CURRENT_DESKTOP")
    hl.exec_cmd("/usr/lib/polkit-kde-authentication-agent-1")
    hl.exec_cmd("dunst")
    hl.exec_cmd("swayosd-server")
    hl.exec_cmd("waybar")
    hl.exec_cmd("hyprpaper")
    hl.exec_cmd("hypridle")

    -- --eventgen uinput: otherwise antimicrox may pick XTest based on XDG_SESSION_TYPE
    hl.exec_cmd("antimicrox --hidden --eventgen uinput --profile ~/.config/antimicrox/generic.gamecontroller.amgp")

    -- this is kind of brittle and might also not be needed since TVs generally only have 1 monitor
    hl.exec_cmd("xrandr --output $(hyprctl monitors -j | jq -r '.[0] | .name') --primary")

    -- Steam Big Picture never released the controller, so it's disabled
    -- hl.exec_cmd("steam -tenfoot", { workspace = "1 silent" })
    -- hl.exec_cmd("heroic", { workspace = "1 silent" })
    hl.exec_cmd("lutris", { workspace = "1 silent" })
    hl.exec_cmd("rpcs3", { workspace = "1 silent" })
    -- hl.exec_cmd("retroarch", { workspace = "1 silent" })

    hl.exec_cmd("flatpak run org.jellyfin.JellyfinDesktop --fullscreen --tv", { workspace = "1 silent" })

    hl.exec_cmd("gtk-launch youtube-pwa", { workspace = "1 silent" })
end)
