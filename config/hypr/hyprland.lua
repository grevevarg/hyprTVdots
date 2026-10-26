-- Lua config (Hyprland 0.55+; written for 0.56.2). If hyprland.lua exists it takes precedence over hyprland.conf.
-- Each require() runs in its own protected scope, so a runtime error in one module does not abort the others.

require("modules.env")
require("modules.monitors")
require("modules.autostart")
require("modules.input")
require("modules.cursor")
require("modules.general")
require("modules.misc")
require("modules.decorations")
require("modules.animations")
require("modules.windowrules")
-- require("modules.layerrules")
require("modules.binds")
