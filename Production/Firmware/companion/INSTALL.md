# maestro OLED app — install guide

This little app makes your **maestro macropad's screen** show the song you're
playing (Spotify or any media), and the time & date when nothing is playing.

It's a small Python script — you run it from source, so you can see exactly what
it does.

## Install (Windows)

1. Install **Python 3.9+** from [python.org](https://www.python.org/downloads/)
   (tick *"Add Python to PATH"* during setup). Use this Python, **not** the one
   bundled with QMK MSYS.
2. Open PowerShell in this `companion` folder and install the dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Run it:
   ```powershell
   python maestro_oled.py
   ```
   A small window shows the status ("Connected to maestro" once your macropad is
   plugged in).
4. Play something on Spotify — it appears on the macropad's screen.

> Prefer a double-clickable app with no console window? You can build your own
> `.exe` from this source — see **Build a standalone .exe** in
> [README.md](README.md).

## Start it automatically at login

So the screen "just works" every time you turn on your PC:

1. Press `Win + R`, type `shell:startup`, press Enter.
2. Create a shortcut in that folder pointing to:
   ```
   pythonw.exe "<path-to-this-folder>\maestro_oled.py"
   ```
   (`pythonw.exe` runs it quietly with no console window.)

Now it launches quietly whenever you log in.

## What it shows

```
While playing                  When idle
┌─────────────────────┐        ┌─────────────────────┐
│ Song title           │        │ 14:35:07            │
│ Artist               │        │ Tue 01 Jul 2026     │
│                      │        │                     │
│ Spotify              │        │ maestro             │
└─────────────────────┘        └─────────────────────┘
```

## Notes

- It reads media playing **on this PC** (Spotify desktop app, browsers, etc.).
- If the macropad isn't plugged in, the app just waits for it — no harm done.
- To stop it, close the window (or end the `python` process in Task Manager).
