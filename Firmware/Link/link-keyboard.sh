#!/usr/bin/env bash
# Links this repo's `maestro` keyboard into your local QMK tree so that
# `qmk compile -kb maestro -km default` builds straight from this repo.
#
# macOS / Linux:
#   cd Firmware/Link
#   ./link-keyboard.sh                     # auto-detects ~/qmk_firmware
#   ./link-keyboard.sh /path/to/qmk_firmware
set -euo pipefail

# This script lives in Firmware/Link/; the keyboard is one level up in Firmware/keyboards/maestro.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE="$SCRIPT_DIR/../keyboards/maestro"
[ -d "$SOURCE" ] && SOURCE="$(cd "$SOURCE" && pwd)"   # normalize away the ".." when it exists
QMK_HOME="${1:-$HOME/qmk_firmware}"
DEST="$QMK_HOME/keyboards/maestro"

[ -f "$SOURCE/keyboard.json" ] || { echo "Keyboard source not found at $SOURCE" >&2; exit 1; }
[ -d "$QMK_HOME" ] || { echo "QMK not found at $QMK_HOME. Run 'qmk setup' first." >&2; exit 1; }

# `rm` on a symlink removes only the link, not the target.
[ -e "$DEST" ] && rm -rf "$DEST"

ln -s "$SOURCE" "$DEST"

echo "Linked: $DEST"
echo "     -> $SOURCE"
echo
echo "Now build with:  qmk compile -kb maestro -km default"
