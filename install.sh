#!/bin/bash

set -e

### Пакеты, которые будут установлены
packages=(
    bspwm sxhkd kitty picom dunst feh rofi zsh \
    papirus-icon-theme ttf-jetbrains-mono unzip wget curl git
)

### Функция: установка пакетов
install_packages() {
    echo "[+] Установка базовых пакетов..."
    sudo pacman -Syu --noconfirm "${packages[@]}"
}

### Функция: установка Oh My Zsh
install_ohmyzsh() {
    if [ ! -d "$HOME/.oh-my-zsh" ]; then
        echo "[+] Установка Oh My Zsh..."
        sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
    fi
}

### Функция: копирование конфигов
copy_configs() {
    echo "[+] Копирование конфигураций..."
    mkdir -p $HOME/.config
    cp -r .config/* $HOME/.config/
    cp .zshrc $HOME/.zshrc
}

### BSPWM: стартовые настройки
setup_bspwm() {
    echo "[+] Настройка bspwm и sxhkd..."
    mkdir -p $HOME/.config/bspwm $HOME/.config/sxhkd

    cat > $HOME/.config/bspwm/bspwmrc <<EOF
#!/bin/sh

# Запуск фоновых приложений
pgrep -x sxhkd > /dev/null || sxhkd &

# Настройка рабочих столов
bspc monitor -d 1 2 3 4 5 6 7 8 9 10

# Настройки поведения окон
bspc config border_width         2
bspc config window_gap           10
bspc config split_ratio          0.5
bspc config borderless_monocle  true
bspc config gapless_monocle     true
bspc config focus_follows_pointer true
EOF
    chmod +x $HOME/.config/bspwm/bspwmrc

    cat > $HOME/.config/sxhkd/sxhkdrc <<EOF
# Запуск терминала
super + Return
    kitty

# Запуск rofi
super + d
    rofi -show drun

# Перезапуск sxhkd
super + Escape
    pkill -USR1 -x sxhkd

# Перемещение фокуса по направлению
super + {h,j,k,l}
    bspc node -f {west,south,north,east}

# Перемещение окон
super + shift + {h,j,k,l}
    bspc node -s {west,south,north,east}

# Удаление окна
super + w
    bspc node -c

# Перезапуск bspwm
super + alt + r
    bspc wm -r
EOF
}

### Запуск
install_packages
install_ohmyzsh
copy_configs
setup_bspwm

echo "[✓] Установка завершена. Перезагрузите сессию bspwm или войдите под ним."
