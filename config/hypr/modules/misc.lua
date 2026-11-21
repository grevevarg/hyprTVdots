hl.config({
    misc = {
        disable_hyprland_logo    = true,
        disable_splash_rendering = true,
        mouse_move_enables_dpms  = true,
        -- HTPC: windows that request activation (Steam, launchers handing off to games) take focus.
        focus_on_activate         = true,
        -- A new window opened over a fullscreen one takes over fullscreen instead of hiding behind it.
        on_focus_under_fullscreen = 1,
    },
    -- debug = { vfr = true },

    -- sry vaxry but its gonna be annoying to deal with these on a tv
    ecosystem = {
        no_update_news  = true,
        no_donation_nag = true,
    },
})
