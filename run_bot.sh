#!/bin/bash

# Script para iniciar o bot do Telegram e mantê-lo em execução contínua
# Autor: Manus AI
# Data: 16/04/2025

# Diretório do bot
BOT_DIR="$(dirname "$(readlink -f "$0")")"
cd "$BOT_DIR"

# Ativa o ambiente virtual
source venv/bin/activate

# Função para iniciar o bot
start_bot() {
    echo "Iniciando o bot do Telegram..."
    python bot.py
}

# Função para verificar se o bot está em execução
is_bot_running() {
    pgrep -f "python bot.py" > /dev/null
    return $?
}

# Função para reiniciar o bot se ele parar
monitor_and_restart() {
    while true; do
        if ! is_bot_running; then
            echo "Bot não está em execução. Reiniciando..."
            start_bot &
        fi
        sleep 60  # Verifica a cada minuto
    done
}

# Inicia o bot
start_bot &

# Monitora e reinicia se necessário
monitor_and_restart
