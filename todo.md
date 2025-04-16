# Lista de Tarefas para o Bot do Telegram

## Configuração e Desenvolvimento Básico
- [x] Confirmar requisitos com o usuário
- [x] Configurar ambiente de desenvolvimento
- [x] Criar bot básico do Telegram
  - [x] Registrar um novo bot com BotFather (bot já existente: Radarfinanceiro-bot)
  - [x] Implementar estrutura básica do bot
  - [x] Criar comandos básicos (/start, /help, /status, /preco, /config)

## Funcionalidades Principais
- [x] Implementar monitoramento de preços
  - [x] Configurar API para BTC/USD
  - [x] Configurar API para USD/BRL
  - [x] Implementar função de verificação a cada 5 minutos
- [x] Implementar sistema de alertas
  - [x] Detectar variações de 2% ou mais
  - [x] Criar formato de mensagem para alertas
- [x] Implementar busca de notícias
  - [x] Configurar API para busca de notícias em português
  - [x] Configurar API para busca de notícias em inglês
  - [x] Correlacionar notícias com variações de preço

## Implantação e Manutenção
- [x] Configurar execução contínua
  - [x] Implementar mecanismo para execução 24/7
  - [x] Configurar serviço systemd para inicialização automática
  - [x] Criar scripts de instalação e gerenciamento
  - [ ] Configurar sistema de logs
- [x] Testar bot completo
  - [x] Verificar todas as funcionalidades
  - [x] Testar em diferentes cenários
- [x] Entregar bot e documentação
  - [x] Preparar documentação de uso
  - [x] Preparar documentação técnica
  - [x] Instruções para integração futura com Google Sheets
