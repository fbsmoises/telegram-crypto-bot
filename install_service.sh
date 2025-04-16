#!/bin/bash

# Script para instalar o serviço do bot do Telegram
# Autor: Manus AI
# Data: 16/04/2025

# Verifica se está sendo executado como root
if [ "$EUID" -ne 0 ]; then
  echo "Este script precisa ser executado como root (sudo)."
  exit 1
fi

# Diretório do bot
BOT_DIR="/home/ubuntu/telegram_bot"
SERVICE_FILE="$BOT_DIR/telegrambot.service"
DEST_SERVICE_FILE="/etc/systemd/system/telegrambot.service"

# Copia o arquivo de serviço para o diretório do systemd
echo "Copiando arquivo de serviço..."
cp "$SERVICE_FILE" "$DEST_SERVICE_FILE"

# Recarrega o systemd para reconhecer o novo serviço
echo "Recarregando systemd..."
systemctl daemon-reload

# Habilita o serviço para iniciar na inicialização do sistema
echo "Habilitando o serviço..."
systemctl enable telegrambot.service

# Inicia o serviço
echo "Iniciando o serviço..."
systemctl start telegrambot.service

# Verifica o status do serviço
echo "Status do serviço:"
systemctl status telegrambot.service

echo ""
echo "Instalação concluída! O bot agora está configurado para execução contínua 24/7."
echo "Use os seguintes comandos para gerenciar o serviço:"
echo "  - sudo systemctl start telegrambot.service   # Iniciar o serviço"
echo "  - sudo systemctl stop telegrambot.service    # Parar o serviço"
echo "  - sudo systemctl restart telegrambot.service # Reiniciar o serviço"
echo "  - sudo systemctl status telegrambot.service  # Verificar o status do serviço"
