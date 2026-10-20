'''
tests for bin/antimicrox-hyprdaemon. no Hyprland, antimicrox or D-Bus needed: set/presence calls are stubbed.

run from the repo root: python3 -m unittest discover -s tests -v
'''

import importlib.machinery
import importlib.util
import logging
import os
import subprocess
import unittest
from unittest import mock

DAEMON_PATH = os.path.join(os.path.dirname(__file__), "..", "bin", "antimicrox-hyprdaemon")
_loader = importlib.machinery.SourceFileLoader("antimicrox_hyprdaemon", DAEMON_PATH)
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
daemon = importlib.util.module_from_spec(_spec)
_loader.exec_module(daemon)

Set = daemon.ControllerSet

# HAND-WRITTEN fixtures in Hyprland socket2 format (EVENT>>DATA, one per line), not recorded from a live session
ADDR = "55d3c0a1b2c0"
JELLYFIN_FOCUS = f"activewindowv2>>{ADDR}\nactivewindow>>org.jellyfin.JellyfinDesktop,Jellyfin\n"
HELIUM_FOCUS = "activewindow>>helium,New Tab - Helium\nactivewindowv2>>55d3c0a1b2d0\n"
LUTRIS_FOCUS = "activewindow>>net.lutris.Lutris,Lutris\n"
GAME_FOCUS = "activewindow>>SomeGame.x86_64,Some Game\n"
NOTHING_FOCUSED = "activewindow>>,\nactivewindowv2>>\n"
OTHER_EVENTS = f"workspace>>1\nworkspacev2>>1,1\nwindowtitlev2>>{ADDR},Jellyfin, now playing\n"


class FakeAntimicrox:
    '''
    stands in for the gdbus calls: owner is the unique bus name (None = not running)
    '''
    def __init__(self, owner=":1.10"):
        self.owner = owner
        self.calls = []          # (device_id, set_id) of every set attempt
        self.fail_next = 0       # number of upcoming set calls that fail
        self.presence_checks = 0

    def set(self, device_id, set_id):
        self.calls.append((device_id, set_id))
        if self.fail_next:
            self.fail_next -= 1
            return False
        return self.owner is not None

    def presence(self):
        self.presence_checks += 1
        return self.owner

    def get(self, device_id):
        return Set.MEDIA


def make(owner=":1.10"):
    fake = FakeAntimicrox(owner)
    controller = daemon.Controller(fake.set, fake.presence, fake.get)
    controller.start()
    return fake, controller, daemon.LineBuffer()


def feed(controller, buffer, data):
    for line in buffer.feed(data.encode()):
        event = daemon.parse_activewindow(line)
        if event is not None:
            controller.on_focus(*event)


def set_ids(fake):
    return [set_id for _, set_id in fake.calls]


class ParsingTests(unittest.TestCase):
    def test_multi_event_single_read(self):
        buffer = daemon.LineBuffer()
        lines = buffer.feed((OTHER_EVENTS + JELLYFIN_FOCUS).encode())
        self.assertEqual(len(lines), 5)
        events = [e for e in map(daemon.parse_activewindow, lines) if e]
        self.assertEqual(events, [("org.jellyfin.JellyfinDesktop", "Jellyfin")])

    def test_partial_line_across_two_reads(self):
        buffer = daemon.LineBuffer()
        self.assertEqual(buffer.feed(b"workspace>>1\nactivewindow>>org.jelly"), ["workspace>>1"])
        self.assertEqual(buffer.feed(b"fin.JellyfinDesktop,Jellyfin\n"),
                         ["activewindow>>org.jellyfin.JellyfinDesktop,Jellyfin"])
        self.assertEqual(buffer.feed(b""), [])

    def test_multibyte_char_split_across_reads(self):
        buffer = daemon.LineBuffer()
        data = "activewindow>>helium,Café\n".encode()
        cut = data.index("é".encode()) + 1
        self.assertEqual(buffer.feed(data[:cut]), [])
        self.assertEqual(buffer.feed(data[cut:]), ["activewindow>>helium,Café"])

    def test_activewindowv2_is_never_a_class(self):
        self.assertIsNone(daemon.parse_activewindow(f"activewindowv2>>{ADDR}"))
        self.assertIsNone(daemon.parse_activewindow(f"windowtitlev2>>{ADDR},title"))

    def test_title_with_commas(self):
        self.assertEqual(daemon.parse_activewindow("activewindow>>net.lutris.Lutris,Lutris, Games, Library"),
                         ("net.lutris.Lutris", "Lutris, Games, Library"))
        self.assertEqual(daemon.parse_activewindow("activewindow>>rpcs3,FPS: 60, RPCS3 0.0.38"),
                         ("rpcs3", "FPS: 60, RPCS3 0.0.38"))

    def test_empty_class(self):
        self.assertEqual(daemon.parse_activewindow("activewindow>>,"), ("", ""))


class SelectSetTests(unittest.TestCase):
    def test_table(self):
        cases = [
            ("org.jellyfin.JellyfinDesktop", "Jellyfin", Set.MEDIA),
            ("chrome-youtube.com__tv-Default", "YouTube on TV", Set.MEDIA),
            ("helium", "New Tab", Set.GENERIC),
            ("com.mitchellh.ghostty", "~", Set.GENERIC),
            ("net.lutris.Lutris", "Lutris", Set.GENERIC),
            ("net.lutris.Lutris", "Some game", Set.NULL_SET),
            ("rpcs3", "FPS: 60, RPCS3 0.0.38", Set.GENERIC),
            ("rpcs3", "Game window", Set.NULL_SET),
            ("steam", "Steam", Set.NULL_SET),
            ("antimicrox", "antimicrox", Set.GENERIC),
            ("SomeGame.x86_64", "Some Game", Set.NULL_SET),   # I5: unmatched -> NULL_SET by design
            ("Alacritty", "Alacritty", Set.NULL_SET),
            (ADDR, "", Set.NULL_SET),
            ("", "", Set.NULL_SET),
        ]
        for window_class, title, expected in cases:
            with self.subTest(window_class=window_class, title=title):
                self.assertEqual(daemon.select_set(window_class, title), expected)


class ControllerTests(unittest.TestCase):
    def test_multi_event_read_applies_class_not_address(self):
        fake, controller, buffer = make()
        feed(controller, buffer, JELLYFIN_FOCUS)
        self.assertEqual(set_ids(fake), [Set.MEDIA])
        self.assertEqual(fake.calls[0][0], 0)   # I4: device index still hardcoded

    def test_activewindowv2_alone_does_nothing(self):
        fake, controller, buffer = make()
        feed(controller, buffer, f"activewindowv2>>{ADDR}\n")
        self.assertEqual(fake.calls, [])

    def test_partial_line_applies_once_complete(self):
        fake, controller, buffer = make()
        feed(controller, buffer, "activewindow>>org.jellyfin.Jelly")
        self.assertEqual(fake.calls, [])
        feed(controller, buffer, "finDesktop,Jellyfin\n")
        self.assertEqual(set_ids(fake), [Set.MEDIA])

    def test_title_with_commas_keeps_class(self):
        fake, controller, buffer = make()
        feed(controller, buffer, "activewindow>>net.lutris.Lutris,Lutris, Games\n")
        self.assertEqual(set_ids(fake), [Set.GENERIC])
        self.assertEqual(controller.current, ("net.lutris.Lutris", "Lutris, Games"))

    def test_duplicate_focus_same_set_one_call(self):
        fake, controller, buffer = make()
        feed(controller, buffer, JELLYFIN_FOCUS * 3)
        feed(controller, buffer, "activewindow>>chrome-youtube.com__tv-Default,YouTube on TV\n")
        self.assertEqual(set_ids(fake), [Set.MEDIA])
        feed(controller, buffer, HELIUM_FOCUS + LUTRIS_FOCUS)
        self.assertEqual(set_ids(fake), [Set.MEDIA, Set.GENERIC])

    def test_generic_media_null_switching(self):
        fake, controller, buffer = make()
        feed(controller, buffer, HELIUM_FOCUS + JELLYFIN_FOCUS + GAME_FOCUS + HELIUM_FOCUS)
        self.assertEqual(set_ids(fake), [Set.GENERIC, Set.MEDIA, Set.NULL_SET, Set.GENERIC])

    def test_failed_call_not_remembered_then_retried(self):
        fake, controller, buffer = make()
        fake.fail_next = 1
        feed(controller, buffer, JELLYFIN_FOCUS)
        self.assertIsNone(controller.last_applied)
        self.assertEqual(controller.owner, ":1.10")   # still present after the re-check
        feed(controller, buffer, JELLYFIN_FOCUS)
        self.assertEqual(set_ids(fake), [Set.MEDIA, Set.MEDIA])
        self.assertEqual(controller.last_applied, Set.MEDIA)
        feed(controller, buffer, JELLYFIN_FOCUS)
        self.assertEqual(len(fake.calls), 2)

    def test_empty_class_gets_null_set(self):
        fake, controller, buffer = make()
        feed(controller, buffer, HELIUM_FOCUS + NOTHING_FOCUSED)
        self.assertEqual(set_ids(fake), [Set.GENERIC, Set.NULL_SET])

    def test_absent_skips_calls_one_check_per_focus_change(self):
        fake, controller, buffer = make(owner=None)
        checks_after_start = fake.presence_checks
        feed(controller, buffer, JELLYFIN_FOCUS * 3 + HELIUM_FOCUS)
        self.assertEqual(fake.calls, [])
        self.assertEqual(fake.presence_checks - checks_after_start, 2)   # jellyfin, helium

    def test_absent_to_present_via_poll_applies_current_window(self):
        fake, controller, buffer = make(owner=None)
        feed(controller, buffer, JELLYFIN_FOCUS)
        controller.poll()
        self.assertEqual(fake.calls, [])
        fake.owner = ":1.20"
        with self.assertLogs(daemon.logger, logging.INFO) as logs:
            controller.poll()
        self.assertEqual(set_ids(fake), [Set.MEDIA])
        self.assertEqual(sum("antimicrox is present" in m for m in logs.output), 1)

    def test_absent_to_present_via_focus_change(self):
        fake, controller, buffer = make(owner=None)
        feed(controller, buffer, JELLYFIN_FOCUS)
        fake.owner = ":1.20"
        feed(controller, buffer, HELIUM_FOCUS)
        self.assertEqual(set_ids(fake), [Set.GENERIC])

    def test_present_to_absent_logs_once(self):
        fake, controller, buffer = make()
        feed(controller, buffer, JELLYFIN_FOCUS)
        fake.owner = None
        with self.assertLogs(daemon.logger, logging.DEBUG) as logs:
            feed(controller, buffer, HELIUM_FOCUS)          # set fails -> re-check -> absent
            feed(controller, buffer, GAME_FOCUS + LUTRIS_FOCUS + JELLYFIN_FOCUS)
            controller.poll()
            controller.poll()
        gone = [m for m in logs.output if "antimicrox is gone" in m]
        self.assertEqual(len(gone), 1)
        self.assertIsNone(controller.owner)
        self.assertEqual(set_ids(fake), [Set.MEDIA, Set.GENERIC])   # no calls after it went away
        self.assertFalse(any("ERROR" in m for m in logs.output[1:]))

    def test_present_to_absent_via_poll(self):
        fake, controller, buffer = make()
        feed(controller, buffer, JELLYFIN_FOCUS)
        fake.owner = None
        with self.assertLogs(daemon.logger, logging.WARNING) as logs:
            controller.poll()
            controller.poll()
        self.assertEqual(len(logs.output), 1)

    def test_restart_resets_memory(self):
        fake, controller, buffer = make()
        feed(controller, buffer, JELLYFIN_FOCUS)
        fake.owner = ":1.30"   # antimicrox restarted between two polls
        controller.poll()
        self.assertEqual(set_ids(fake), [Set.MEDIA, Set.MEDIA])

    def test_no_focus_seen_yet_present_does_nothing(self):
        fake, controller, buffer = make(owner=None)
        fake.owner = ":1.20"
        controller.poll()
        self.assertEqual(fake.calls, [])

    def test_pause_and_resume(self):
        fake, controller, buffer = make()
        feed(controller, buffer, JELLYFIN_FOCUS)
        controller.toggle_pause()
        feed(controller, buffer, GAME_FOCUS)
        self.assertEqual(set_ids(fake), [Set.MEDIA, Set.GENERIC])
        controller.toggle_pause()
        self.assertEqual(set_ids(fake), [Set.MEDIA, Set.GENERIC, Set.MEDIA])   # fake.get returns MEDIA


class PresenceQueryTests(unittest.TestCase):
    def test_owner_parsed(self):
        done = subprocess.CompletedProcess([], 0, stdout="(':1.42',)\n", stderr="")
        with mock.patch.object(daemon.subprocess, "run", return_value=done) as run:
            self.assertEqual(daemon.get_antimicrox_owner(), ":1.42")
        args = run.call_args.args[0]
        self.assertIn("org.freedesktop.DBus.GetNameOwner", args)
        self.assertEqual(args[-1], "io.github.antimicrox")

    def test_absent(self):
        error = subprocess.CalledProcessError(1, "gdbus", stderr="NameHasNoOwner")
        with mock.patch.object(daemon.subprocess, "run", side_effect=error):
            self.assertIsNone(daemon.get_antimicrox_owner())


if __name__ == "__main__":
    unittest.main()
