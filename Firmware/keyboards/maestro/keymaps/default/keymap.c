// Copyright 2026 Yash (@yaasshh09)
// SPDX-License-Identifier: GPL-2.0-or-later

#include QMK_KEYBOARD_H
#include <string.h>

#ifdef RAW_ENABLE
#    include "raw_hid.h"
#endif


#define ENCODER_SW_PIN     GP2
#define ENCODER_SW_KEYCODE KC_MUTE

const uint16_t PROGMEM keymaps[][MATRIX_ROWS][MATRIX_COLS] = {
    [0] = LAYOUT_ortho_2x3(
        C(KC_Z),  C(KC_C),  C(KC_V),
        C(KC_X),  C(KC_Y),  C(KC_S)
    )
};

#ifdef ENCODER_ENABLE
bool encoder_update_user(uint8_t index, bool clockwise) {
    tap_code(clockwise ? KC_VOLU : KC_VOLD);
    return false;
}
#endif

void keyboard_post_init_user(void) {
    // Encoder switch: input with internal pull-up, switch shorts to GND (active-low).
    gpio_set_pin_input_high(ENCODER_SW_PIN);
}

void housekeeping_task_user(void) {
    static bool     pressed  = false;
    static uint16_t debounce = 0;

    bool reading = !gpio_read_pin(ENCODER_SW_PIN); // active-low
    if (reading != pressed && timer_elapsed(debounce) > 5) {
        pressed  = reading;
        debounce = timer_read();
        if (pressed) {
            register_code(ENCODER_SW_KEYCODE);
        } else {
            unregister_code(ENCODER_SW_KEYCODE);
        }
    }
}

#define OLED_TEXT_COLS 21
#define OLED_TEXT_ROWS 4
#define HOST_TIMEOUT_MS 5000

#ifdef RAW_ENABLE
static char     host_screen[OLED_TEXT_ROWS][OLED_TEXT_COLS + 1] = {0};
static uint32_t host_last_update                                 = 0;

// Each report: data[0] = row index (0-3), data[1..] = ASCII text for that row.
void raw_hid_receive(uint8_t *data, uint8_t length) {
    uint8_t row = data[0];
    if (row < OLED_TEXT_ROWS) {
        memset(host_screen[row], 0, sizeof(host_screen[row]));
        for (uint8_t i = 0; i < OLED_TEXT_COLS && (i + 1) < length; i++) {
            char c = (char)data[i + 1];
            if (c == 0) {
                break;
            }
            host_screen[row][i] = c;
        }
    }
    host_last_update = timer_read32();
#    ifdef OLED_ENABLE
    oled_on(); // keep the screen awake while the app is feeding it
#    endif
}
#endif

#ifdef OLED_ENABLE
oled_rotation_t oled_init_user(oled_rotation_t rotation) {
    return OLED_ROTATION_0;
}

static void oled_write_padded(const char *text) {
    uint8_t len = (uint8_t)strlen(text);
    oled_write(text, false);
    for (uint8_t c = len; c < OLED_TEXT_COLS; c++) {
        oled_write_char(' ', false); // clear any stale characters on the line
    }
}

bool oled_task_user(void) {
#    ifdef RAW_ENABLE
    if (timer_elapsed32(host_last_update) < HOST_TIMEOUT_MS) {
        for (uint8_t r = 0; r < OLED_TEXT_ROWS; r++) {
            oled_set_cursor(0, r);
            oled_write_padded(host_screen[r]);
        }
        return false;
    }
#    endif
    // Companion app not running -> static fallback.
    oled_write_P(PSTR("maestro\n"), false);
    oled_write_P(PSTR("\n"), false);
    oled_write_P(PSTR("turn: vol\n"), false);
    oled_write_P(PSTR("press: mute"), false);
    return false;
}
#endif
