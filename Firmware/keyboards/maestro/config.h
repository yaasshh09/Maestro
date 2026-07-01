// Copyright 2026 Yash (@yaasshh09)
// SPDX-License-Identifier: GPL-2.0-or-later

#pragma once

/* Enter the RP2040 UF2 bootloader by double-tapping the reset/BOOT button. */
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET
#define RP2040_BOOTLOADER_DOUBLE_TAP_RESET_TIMEOUT 500U

/* 0.91" SSD1306 OLED is wired to D4 (SDA) / D5 (SCL) = GP6 / GP7 = I2C1. */
#define I2C_DRIVER I2CD1
#define I2C1_SDA_PIN GP6
#define I2C1_SCL_PIN GP7

#ifdef OLED_ENABLE
#    define OLED_DISPLAY_128X32
#    define OLED_TIMEOUT 60000
#    define OLED_BRIGHTNESS 128
#endif
