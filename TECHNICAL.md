# Documentação Técnica - Radar Financeiro Bot

## Visão Geral da Arquitetura

O Radar Financeiro Bot foi desenvolvido com uma arquitetura modular, separando as diferentes funcionalidades em módulos independentes para facilitar a manutenção e extensão. A arquitetura é composta pelos seguintes componentes principais:

### Componentes Principais

1. **Bot Principal (bot.py)**
   - Gerencia a interface com o Telegram
   - Processa comandos dos usuários
   - Coordena os outros módulos

2. **Monitor de Preços (price_monitor.py)**
   - Obtém preços atuais dos pares BTC/USD e USD/BRL
   - Armazena histórico de preços
   - Calcula variações percentuais

3. **Agendador (scheduler.py)**
   - Verifica preços periodicamente (a cada 5 minutos)
   - Detecta variações significativas (≥ 2%)
   - Dispara alertas quando necessário

4. **Buscador de Notícias (news_searcher.py)**
   - Busca notícias relacionadas às variações de preço
   - Suporta busca em português e inglês
   - Formata mensagens com as notícias encontradas

5. **Sistema de Execução Contínua**
   - Script de execução (run_bot.sh)
   - Serviço systemd (telegrambot.service)
   - Script de instalação (install_service.sh)

## Fluxo de Dados

1. O agendador verifica os preços a cada 5 minutos usando o monitor de preços
2. Se uma variação ≥ 2% for detectada, um alerta é gerado
3. O buscador de notícias é acionado para encontrar notícias relacionadas
4. O bot envia o alerta e as notícias para todos os usuários registrados

## Detalhes de Implementação

### Monitor de Preços

```python
# Obtém preços da API do Yahoo Finance
def get_btc_usd_price(self):
    url = "https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD"
    params = {"interval": "1d", "range": "1d"}
    headers = {"User-Agent": "Mozilla/5.0..."}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()
    price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
    # Armazena no histórico e retorna
    return price, timestamp
```

### Sistema de Alertas

```python
# Verifica variações de preço
async def check_prices(self):
    data = self.monitor.get_price_data()
    btc_usd = data["BTC/USD"]
    
    if btc_usd["variation"] is not None and abs(btc_usd["variation"]) >= self.alert_threshold:
        # Formata e envia alerta
        message = f"{emoji} ALERTA DE VARIAÇÃO {emoji}\n\n..."
        # Busca e envia notícias relacionadas
        await send_news_for_alert(self.bot, self.chat_ids, "BTC/USD", btc_usd["variation"])
```

### Buscador de Notícias

```python
# Busca notícias para um par específico
def search_news_for_pair(self, pair, variation_pct):
    # Define termos de busca baseados no par e direção da variação
    if pair == "BTC/USD":
        query_pt = "Bitcoin BTC criptomoeda preço variação"
        query_en = "Bitcoin BTC cryptocurrency price movement"
    # Busca tweets e notícias em português e inglês
    tweets_pt = self._search_twitter(query_pt, lang="pt")
    news_en = self._search_news_api(query_en, language="en")
    # Combina e retorna resultados
```

### Gerenciamento de Usuários

```python
# Registra um usuário para receber alertas
def save_user(chat_id, username=None, first_name=None):
    users = load_users()
    # Verifica se o usuário já está registrado
    for user in users:
        if user.get("chat_id") == chat_id:
            return False
    # Adiciona o novo usuário
    users.append({
        "chat_id": chat_id,
        "username": username,
        "first_name": first_name,
        "registered_at": str(asyncio.get_event_loop().time())
    })
    # Salva a lista atualizada
```

## Armazenamento de Dados

O bot utiliza arquivos JSON para armazenar dados persistentes:

1. **users.json** - Lista de usuários registrados para receber alertas
2. **btc_usd_history.json** - Histórico de preços do par BTC/USD
3. **usd_brl_history.json** - Histórico de preços do par USD/BRL
4. **alerts.json** - Histórico de alertas enviados
5. **news.json** - Histórico de notícias encontradas

## Tratamento de Erros

O bot implementa tratamento de erros em vários níveis:

1. **Nível de API** - Tratamento de falhas nas chamadas às APIs externas
2. **Nível de Comando** - Tratamento de erros nos comandos do usuário
3. **Nível de Sistema** - Monitoramento e reinicialização automática

Em caso de falha na obtenção de preços, o sistema utiliza valores simulados para continuar funcionando.

## Logging

O sistema de logging é configurado para armazenar informações detalhadas:

```python
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='/home/ubuntu/telegram_bot/logs/bot.log',
    filemode='a'
)
```

## Integração Futura com Google Sheets

Para implementar a integração com Google Sheets, será necessário:

1. Instalar a biblioteca gspread: `pip install gspread oauth2client`
2. Criar credenciais de API no Google Cloud Platform
3. Implementar um novo módulo (sheets_integration.py) com funções para:
   - Conectar à API do Google Sheets
   - Registrar variações de preço
   - Registrar notícias correlacionadas
   - Atualizar planilhas automaticamente

## Considerações de Segurança

1. O token do bot está armazenado diretamente no código-fonte
2. Para um ambiente de produção, recomenda-se:
   - Mover o token para variáveis de ambiente ou arquivo de configuração separado
   - Implementar autenticação para comandos administrativos
   - Adicionar rate limiting para evitar abuso

## Testes

O sistema inclui testes automatizados (test_bot.py) que verificam:

1. Estrutura do bot (arquivos necessários)
2. Monitor de preços (obtenção de preços)
3. Buscador de notícias (busca e formatação)
4. Agendador (configuração e funcionamento)

## Limitações Conhecidas

1. As APIs de notícias são simuladas para fins de demonstração
2. Em um ambiente de produção, seria necessário utilizar APIs reais com autenticação
3. O sistema não implementa cache avançado para reduzir chamadas às APIs
4. Não há mecanismo de backup automático dos dados armazenados
