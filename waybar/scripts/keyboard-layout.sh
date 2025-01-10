#!/bin/bash

# Получение текущей раскладки основной клавиатуры
/usr/bin/hyprctl -j devices | /usr/bin/jq -r '.keyboards[] | select(.main == true) | .active_keymap'

