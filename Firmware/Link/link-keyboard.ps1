# Links this repo's `maestro` keyboard into your local QMK tree so that
# `qmk compile -kb maestro -km default` builds straight from this repo.
#
# Windows only. Run from PowerShell (no admin required - uses a directory junction):
#
#   cd Firmware\Link
#   .\link-keyboard.ps1                              # auto-detects ~\qmk_firmware
#   .\link-keyboard.ps1 -QmkHome "D:\qmk_firmware"   # custom QMK location

param(
    [string]$QmkHome = (Join-Path $HOME "qmk_firmware")
)

$ErrorActionPreference = "Stop"

# This script lives in Firmware\Link\; the keyboard is one level up in Firmware\keyboards\maestro.
$source = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot "..\keyboards\maestro"))
$dest   = Join-Path $QmkHome "keyboards\maestro"

if (-not (Test-Path (Join-Path $source "keyboard.json"))) {
    throw "Keyboard source not found at $source"
}
if (-not (Test-Path $QmkHome)) {
    throw "QMK not found at $QmkHome. Run 'qmk setup' first, or pass -QmkHome <path>."
}

# Remove any existing folder/junction. `rmdir` on a junction removes only the
# link, never the target's contents.
if (Test-Path $dest) {
    cmd /c rmdir "$dest"
}

New-Item -ItemType Junction -Path $dest -Target $source | Out-Null

Write-Host "Linked: $dest"
Write-Host "     -> $source"
Write-Host ""
Write-Host "Now build with:  qmk compile -kb maestro -km default"
