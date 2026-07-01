# maestro

A 6-key (2x3) macropad with a rotary encoder and a 0.91" SSD1306 OLED, driven by
a Seeed **XIAO RP2040**.

* Keyboard Maintainer: [Yash](https://github.com/yaasshh09)
* Hardware Supported: Seeed XIAO RP2040 + 6x SW_Push (1N4148 per key), EC11 rotary
  encoder, 0.91" 128x32 SSD1306 OLED (I2C)

> Note: the PCB uses the generic Seeed XIAO footprint and the schematic
> specifies the **XIAO RP2040**, which this firmware targets. If you socket a
> different XIAO variant, update `processor`, `bootloader`, and the pins in
> `keyboard.json` / `config.h`.

## Wiring (schematic net -> XIAO pad -> RP2040 GPIO)

| Net            | XIAO pad | GPIO  | Role                       |
|----------------|----------|-------|----------------------------|
| COLUMN 0/1/2   | D0/D1/D2 | GP26/GP27/GP28 | Matrix columns    |
| ROW 0          | D3       | GP29  | Matrix row 0               |
| ROW 1          | D9       | GP4   | Matrix row 1               |
| DATA_LINE (SDA)| D4       | GP6   | OLED I2C1 SDA              |
| CLOCK_LINE(SCL)| D5       | GP7   | OLED I2C1 SCL              |
| OUT_A          | D6       | GP0   | Encoder A                  |
| OUT_B          | D7       | GP1   | Encoder B                  |
| SWITCH_P       | D8       | GP2   | Encoder push (direct read) |

Diodes are COL2ROW (anode on the column, cathode on the row).

## Default layout

```
┌─────┬─────┬─────┐
│ Undo│ Copy│Paste│
├─────┼─────┼─────┤
│ Cut │ Redo│ Save│
└─────┴─────┴─────┘
  Encoder: turn = volume, press = mute
```

(Ctrl-based shortcuts; remap freely in `keymaps/default/keymap.c`.)

## OLED (now-playing / clock)

The OLED renders 4 rows of text streamed from a PC companion app over Raw HID:
the current Spotify song while playing, otherwise the time & date. Setup lives in
[`Firmware/companion/`](../../companion/README.md). With the app not running, the OLED shows a
static `maestro` fallback. All layout/formatting is in the companion script — no
reflashing needed to change it.

Make example for this keyboard (after setting up your build environment):

    make maestro:default

Flashing example for this keyboard:

    make maestro:default:flash

See the [build environment setup](https://docs.qmk.fm/#/getting_started_build_tools) and the [make instructions](https://docs.qmk.fm/#/getting_started_make_guide) for more information. Brand new to QMK? Start with our [Complete Newbs Guide](https://docs.qmk.fm/#/newbs).

## Bootloader

Enter the bootloader in 2 ways:

* **Double-tap reset**: quickly double-tap the XIAO RP2040 reset button; it mounts
  as a `RPI-RP2` USB drive — drop the `.uf2` on it.
* **Bootmagic reset**: hold the top-left key (matrix `[0,0]`) while plugging in.
