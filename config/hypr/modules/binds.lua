-- try to set default (unused by any bind)
local TERMINAL = "ghostty"
local BROWSER  = "helium-browser"

-- audio
hl.bind("XF86AudioRaiseVolume", hl.dsp.exec_cmd("swayosd-client --output-volume 5"),           { repeating = true })
hl.bind("XF86AudioLowerVolume", hl.dsp.exec_cmd("swayosd-client --output-volume -5"),          { repeating = true })
hl.bind("XF86AudioMute",        hl.dsp.exec_cmd("swayosd-client --output-volume mute-toggle"), { repeating = true })
hl.bind("XF86AudioPlay",  hl.dsp.exec_cmd("swayosd-client --playerctl play-pause"))
hl.bind("XF86AudioPause", hl.dsp.exec_cmd("swayosd-client --playerctl play-pause"))
hl.bind("XF86AudioNext",  hl.dsp.exec_cmd("swayosd-client --playerctl next"))
hl.bind("XF86AudioPrev",  hl.dsp.exec_cmd("swayosd-client --playerctl previous"))

hl.bind("SUPER + up",   hl.dsp.exec_cmd("swayosd-client --output-volume 5"))
hl.bind("SUPER + down", hl.dsp.exec_cmd("swayosd-client --output-volume -5"))

-- screenshot
hl.bind("Print", hl.dsp.exec_cmd("grim -o ~/Pictures/screenshots/capture_$(date '+%Y-%m-%d_%H-%M-%S').png && notify-send \"Screenshot saved to default folder\""))
-- hl.bind("SUPER + SHIFT + S", hl.dsp.exec_cmd("~/.config/scripts/screenshot_custom"))

hl.bind("SUPER + R", hl.dsp.exec_cmd("killall rofi || rofi -show drun -theme ~/.config/rofi/global/custom.rasi"), { release = true })
-- The controller (antimicrox profile) sends SUPER + F13-F16, keys no app uses, so a press without GUIDE does nothing.
-- xkb maps F13-F16 to the keysyms XF86Tools and XF86Launch5-7. Lua key strings don't take `code:NNN`, so bind the names.
hl.bind("SUPER + XF86Launch6", hl.dsp.exec_cmd("killall rofi || rofi -show drun -theme ~/.config/rofi/global/custom.rasi"), { release = true })

-- below needs a wrapper to make sure that mousenav is automatically set up when activated and then restores previous profile when exited
hl.bind("SUPER + W", hl.dsp.exec_cmd("toggle_waybar"), { release = true })
hl.bind("SUPER + XF86Launch7", hl.dsp.exec_cmd("toggle_waybar"), { release = true })

-- uncreachable from controller atm
-- the gdbus command is used to reset the controller to generic config
-- it assumes you only have one controller plugged in and that the generic profile is the first one
hl.bind("SUPER + Q", hl.dsp.window.close())
hl.bind("SUPER + XF86Launch5", hl.dsp.window.close())
hl.bind("SUPER + SHIFT + S", hl.dsp.exec_cmd("gdbus call --session --dest io.github.antimicrox --object-path /InputDevice/0 --method io.github.antimicrox.InputDevice.setActiveSetNumber 0"))

-- fullscreen/floating stuff
hl.bind("SUPER + F", hl.dsp.window.fullscreen({ action = "toggle" }))
hl.bind("SUPER + XF86Tools", hl.dsp.window.fullscreen({ action = "toggle" }))
-- hl.bind("SUPER + F", hl.dsp.window.float({ action = "toggle" }))

-- monocle
-- release = true: antimicrox re-presses a held button whenever the daemon switches sets, so a press bind loops
hl.bind("SUPER + SHIFT + right", hl.dsp.layout("cyclenext"), { release = true })
hl.bind("SUPER + SHIFT + left",  hl.dsp.layout("cycleprev"), { release = true })

-- below stuff is not relevant for tv system, however im leaving some way to return to workspace 1 in case something fucked up happens
-- special:
-- hl.bind("SUPER + C",         hl.dsp.workspace.toggle_special(""))
-- hl.bind("SUPER + SHIFT + C", hl.dsp.window.move({ workspace = "special" }))

-- switch
hl.bind("SUPER + 1", hl.dsp.focus({ workspace = 1 }))
-- for i = 2, 10 do hl.bind("SUPER + " .. (i % 10), hl.dsp.focus({ workspace = i })) end
-- hl.bind("SHIFT + ALT + right", hl.dsp.focus({ workspace = "e+1" }))
-- hl.bind("SHIFT + ALT + left",  hl.dsp.focus({ workspace = "e-1" }))

-- move
hl.bind("SUPER + SHIFT + 1", hl.dsp.window.move({ workspace = 1 }))
-- for i = 2, 10 do hl.bind("SUPER + SHIFT + " .. (i % 10), hl.dsp.window.move({ workspace = i })) end

-- mouse binding
-- hl.bind("SUPER + mouse:272", hl.dsp.window.drag(),   { mouse = true })
-- hl.bind("SUPER + mouse:273", hl.dsp.window.resize(), { mouse = true })
-- hl.bind("SUPER + mouse_down", hl.dsp.focus({ workspace = "e+1" }))
-- hl.bind("SUPER + mouse_up",   hl.dsp.focus({ workspace = "e-1" }))
