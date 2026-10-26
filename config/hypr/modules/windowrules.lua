-- Regex is RE2; the `negative:` prefix negates.
local function float_class(name, class)
    hl.window_rule({ name = name, match = { class = class }, float = true })
end
local function float_title(name, title)
    hl.window_rule({ name = name, match = { title = title }, float = true })
end

float_class("File-Progress_Float", "file_progress")
float_class("Confirm-Dialog_Float", "confirm")
float_class("Dialog_Float", "dialog")
float_class("Download_Float", "download")

hl.window_rule({
    name  = "Notification_Float_Top_Right",
    match = { class = "^(notification)$" },
    float = true,
    size  = { 64, 256 },
    move  = { "monitor_w*0.9", "15" },
})

float_class("Error_Float", "error")
float_class("Splash_Float", "splash")
float_class("Confirm-Reset_Float", "confirmreset")
float_title("Open-File_Float", "Open File")
float_title("Branch-Dialog_Float", "branchdialog")
float_class("LXAppearance_Float", "Lxappearance")

hl.window_rule({
    name      = "Rofi_Centered_No_Anim",
    match     = { class = "Rofi" },
    float     = true,
    animation = "none",
    center    = true,
})

float_class("File-Roller_Float", "file-roller")
float_title("Picture-in-Picture_Float", "^(Picture-in-Picture)$")

hl.window_rule({
    name  = "Steam_Chat_Float_Centered",
    -- Float + centre every Steam window except the main client and Big Picture (RE2 full match).
    match = { class = "steam", title = "negative:^(Steam|Steam Big Picture Mode)$" },
    float = true,
    center = true,
})

hl.window_rule({
    name  = "Steam_Friends-List_Float",
    match = { class = "steam", title = "Friends List" },
    float = true,
    size  = { 400, 600 },
    move  = { "monitor_w*0.84", "monitor_h*0.02" },
})
