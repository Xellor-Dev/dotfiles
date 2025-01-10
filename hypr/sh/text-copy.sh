#!/bin/bash

SCREENSHOT="/tmp/screenshot.png"
grim -g "$(slurp)" "$SCREENSHOT"
TEXT=$(tesseract "$SCREENSHOT" stdout -l rus+pol+ukr 2>/dev/null)
echo "$TEXT" | wl-copy
notify-send "System" "The text is copied to the clipboard." --icon=/home/xellor/.icons/arch.png --urgency=low