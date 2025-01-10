#!/bin/bash

screenshot="/tmp/blur_screen.png"
grabber="grim"
$grabber $screenshot
convert $screenshot -blur 0x10 $screenshot
swaylock -i $screenshot
rm $screenshot
notify-send "System" "Screen unlocked." --icon=/home/xellor/.icons/arch.png
paplay ~/Sounds/notification2.mp3