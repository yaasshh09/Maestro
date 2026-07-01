#!/usr/bin/env python3
"""maestro OLED companion.

Streams "now playing" (Spotify / any Windows media session) to the maestro
macropad's OLED over Raw HID. When nothing is playing it shows the time & date.

The keyboard just renders whatever 4 rows of text we send, so all formatting
lives here -- tweak this file freely, no reflashing needed.

Requires (use the python.org Python, not the MSYS one):
    pip install hidapi winsdk
"""

import asyncio
import time
from datetime import datetime

import hid  # from the "hidapi" package
from winsdk.windows.media.control import (
    GlobalSystemMediaTransportControlsSessionManager as MediaManager,
    GlobalSystemMediaTransportControlsSessionPlaybackStatus as PlaybackStatus,
)

# --- must match keyboard.json / QMK Raw HID --------------------------------
VID = 0xFEED
PID = 0x0000
USAGE_PAGE = 0xFF60          # QMK Raw HID usage page
USAGE = 0x61                 # QMK Raw HID usage
REPORT_LEN = 32             # RAW_EPSIZE payload size

# --- must match keymap.c ----------------------------------------------------
COLS = 21
ROWS = 4

POLL_SECONDS = 0.4          # how often we refresh the screen / scroll


# ---------------------------------------------------------------------------
# HID transport
# ---------------------------------------------------------------------------
def find_device_path():
    for d in hid.enumerate(VID, PID):
        if d.get("usage_page") == USAGE_PAGE and d.get("usage") == USAGE:
            return d["path"]
    return None


def open_device():
    path = find_device_path()
    if not path:
        return None
    dev = hid.device()
    dev.open_path(path)
    return dev


def send_rows(dev, rows):
    """Send up to ROWS lines; each as one 32-byte report (row index + text)."""
    for i in range(ROWS):
        text = rows[i] if i < len(rows) else ""
        payload = bytearray(REPORT_LEN)
        payload[0] = i
        enc = text.encode("ascii", "replace")[:COLS]
        payload[1:1 + len(enc)] = enc
        # hidapi expects a leading report-ID byte (0x00 = none).
        dev.write(bytes([0x00]) + bytes(payload))


# ---------------------------------------------------------------------------
# Now playing (Windows System Media Transport Controls)
# ---------------------------------------------------------------------------
async def get_now_playing():
    """Return (title, artist) if Spotify (or the current session) is PLAYING."""
    try:
        mgr = await MediaManager.request_async()
    except Exception:
        return None

    session = None
    try:
        for s in mgr.get_sessions():
            try:
                app_id = (s.source_app_user_model_id or "").lower()
            except Exception:
                app_id = ""
            if "spotify" in app_id:
                session = s
                break
    except Exception:
        pass
    if session is None:
        session = mgr.get_current_session()
    if session is None:
        return None

    try:
        if session.get_playback_info().playback_status != PlaybackStatus.PLAYING:
            return None
        props = await session.try_get_media_properties_async()
    except Exception:
        return None

    title = (props.title or "").strip()
    artist = (props.artist or "").strip()
    if not title and not artist:
        return None
    return title, artist


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------
def marquee(text, width, offset):
    """Left-justify if it fits, otherwise scroll it horizontally."""
    if len(text) <= width:
        return text.ljust(width)
    padded = text + "   -   "  # gap between repeats
    start = offset % len(padded)
    return (padded + padded)[start:start + width]


def now_playing_screen(title, artist, offset):
    return [
        marquee(title, COLS, offset),
        marquee(artist, COLS, offset),
        "",
        "Spotify",
    ]


def clock_screen():
    now = datetime.now()
    return [
        now.strftime("%H:%M:%S"),
        now.strftime("%a %d %b %Y"),
        "",
        "maestro",
    ]


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------
async def main():
    dev = None
    offset = 0
    print("maestro OLED companion running. Ctrl+C to quit.")
    while True:
        if dev is None:
            dev = open_device()
            if dev is None:
                print("Waiting for maestro keyboard...")
                time.sleep(2)
                continue
            print("Connected to maestro.")

        np = await get_now_playing()
        rows = now_playing_screen(*np, offset) if np else clock_screen()

        try:
            send_rows(dev, rows)
        except Exception as exc:
            print(f"Lost connection ({exc}); reconnecting...")
            try:
                dev.close()
            except Exception:
                pass
            dev = None
            continue

        offset += 1
        await asyncio.sleep(POLL_SECONDS)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
