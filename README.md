# Radar Financeiro Bot

## Descrição
O Radar Financeiro Bot é um bot do Telegram que monitora os pares de moedas BTC/USD e USD/BRL, alertando sobre variações significativas de preço e buscando automaticamente notícias correlacionadas em português e inglês.

## Funcionalidades

- **Monitoramento de preços**: Verifica os preços de BTC/USD e USD/BRL a cada 5 minutos
- **Sistema de alertas**: Dispara alertas quando há variação de 2% ou mais
- **Busca de notícias**: Busca automaticamente notícias em português e inglês correlacionadas com as variações
- **Execução contínua**: Funciona 24 horas por dia, 7 dias por semana
- **Comandos personalizados**: Inclui comandos para verificar preços, status e configurações

## Comandos Disponíveis

- `/start` - Inicia o bot e registra para receber alertas
- `/help` - Mostra a lista de comandos disponíveis
- `/status` - Verifica o status atual do monitoramento
- `/preco` - Mostra os preços atuais dos pares monitorados
- `/config` - Mostra a configuração atual do bot
- `/parar` - Para de receber alertas
- `/continuar` - Volta a receber alertas

## Requisitos

- Python 3.10 ou superior
- Acesso à internet
- Conta no Telegram
- Token de bot do Telegram (já configurado)

## Instalação

### Configuração do Ambiente

1. Clone o repositório ou extraia os arquivos para um diretório de sua preferência
2. Navegue até o diretório do bot:
   ```
   cd telegram_bot
   ```
3. Crie e ative um ambiente virtual Python:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Instale as dependências:
   ```
   pip install python-telegram-bot requests pandas matplotlib
   ```

### Execução Manual

Para executar o bot manualmente:

```
./run_bot.sh
```

### Instalação como Serviço (Execução 24/7)

Para instalar o bot como um serviço do sistema e garantir execução contínua:

```
sudo ./install_service.sh
```

Após a instalação, o serviço será iniciado automaticamente e configurado para iniciar na inicialização do sistema.

### Gerenciamento do Serviço

- Iniciar o serviço: `sudo systemctl start telegrambot.service`
- Parar o serviço: `sudo systemctl stop telegrambot.service`
- Reiniciar o serviço: `sudo systemctl restart telegrambot.service`
- Verificar status: `sudo systemctl status telegrambot.service`

## Estrutura do Projeto

- `bot.py` - Arquivo principal do bot
- `price_monitor.py` - Módulo para monitoramento de preços
- `scheduler.py` - Módulo para agendamento de verificações
- `news_searcher.py` - Módulo para busca de notícias
- `run_bot.sh` - Script para execução manual
- `install_service.sh` - Script para instalação como serviço
- `telegrambot.service` - Arquivo de configuração do serviço
- `test_bot.py` - Script para testes automatizados
- `data/` - Diretório para armazenamento de dados históricos
- `logs/` - Diretório para armazenamento de logs

## Integração Futura com Google Sheets

O bot foi projetado para futura integração com o Google Sheets para registrar as variações de preço e as notícias correlacionadas. Para implementar esta funcionalidade, será necessário:

1. Criar uma conta de serviço no Google Cloud Platform
2. Habilitar a API do Google Sheets
3. Compartilhar uma planilha com a conta de serviço
4. Implementar a integração usando a biblioteca `gspread`

## Solução de Problemas

### O bot não está respondendo

1. Verifique se o serviço está em execução:
   ```
   sudo systemctl status telegrambot.service
   ```
2. Verifique os logs do sistema:
   ```
   sudo journalctl -u telegrambot.service
   ```
3. Verifique os logs do bot:
   ```
   cat /home/ubuntu/telegram_bot/logs/bot.log
   ```

### Problemas com a API do Yahoo Finance

Se o bot não conseguir obter os preços atuais, ele usará valores simulados para continuar funcionando. Verifique os logs para mais detalhes sobre possíveis erros.

## Suporte

Para suporte ou dúvidas, entre em contato com o desenvolvedor.

## Licença

Este projeto é distribuído sob a licença MIT.
