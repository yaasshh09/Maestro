# maestro OLED companion

A small background program that streams **now-playing** (Spotify / any Windows
media session) and the **clock** to the maestro macropad's OLED over Raw HID.

The firmware just renders 4 rows of text that this app sends, so you can change
the layout/format by editing `maestro_oled.py` alone — no reflashing.

```
Spotify playing                Nothing playing
┌─────────────────────┐        ┌─────────────────────┐
│ Bohemian Rhapsody    │        │ 14:35:07            │
│ Queen                │        │ Tue 01 Jul 2026     │
│                      │        │                     │
│ Spotify              │        │ maestro             │
└─────────────────────┘        └─────────────────────┘
```
(Long titles/artists scroll automatically.)

See [INSTALL.md](INSTALL.md) for the step-by-step end-user guide.

## Requirements

Use the **python.org** Python (3.9+), *not* the MSYS one bundled with QMK.

```powershell
pip install -r requirements.txt
```

This installs `hidapi` (USB) and `winsdk` (Windows "Now Playing" API).

## Run

```powershell
python maestro_oled.py
```

Leave it running. Plug/unplug is handled — it reconnects automatically. When the
app isn't running, the OLED shows a static `maestro` fallback screen.

## Build a standalone .exe (optional)

If you'd rather have a double-clickable app with no Python install, build one
yourself from the source (nothing prebuilt ships in this repo, so you run only
code you can inspect):

```powershell
pip install pyinstaller
pyinstaller --onefile --name maestro-oled --collect-all winsdk maestro_oled.py
# result: dist\maestro-oled.exe
```

## Start automatically at login

Easiest: drop a shortcut in the Startup folder.

1. Press `Win+R`, type `shell:startup`, Enter.
2. Create a shortcut in that folder pointing to:
   ```
   pythonw.exe "C:\Users\yashg\qmk_firmware\keyboards\maestro\companion\maestro_oled.py"
   ```
   (`pythonw.exe` runs it with no console window.)

Or use Task Scheduler with "At log on" if you prefer.

## Customizing the display

Everything is in `maestro_oled.py`:

- `clock_screen()` — what shows when nothing is playing (time/date format).
- `now_playing_screen()` — the song layout (title/artist/labels).
- `POLL_SECONDS` — refresh + scroll speed.
- The OLED is **4 rows × 21 chars**; anything longer scrolls via `marquee()`.

## Notes / limits

- "Now Playing" reads **local** playback on this PC (Spotify desktop, browsers).
  Playback on your phone won't show unless this PC is the active device.
- The constants `VID/PID/USAGE_PAGE/USAGE` must match the firmware. If you change
  the keyboard's USB IDs in `keyboard.json`, update them here too.
