# Instruções para Integração com Google Sheets

Este documento fornece instruções para a futura integração do Radar Financeiro Bot com o Google Sheets, permitindo o registro automático das variações de preço e notícias correlacionadas.

## Pré-requisitos

1. Conta no Google
2. Acesso ao Google Cloud Platform (GCP)
3. Planilha do Google Sheets criada

## Passos para Configuração

### 1. Configurar o Projeto no Google Cloud Platform

1. Acesse o [Console do Google Cloud Platform](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a API do Google Sheets:
   - No menu lateral, vá para "APIs e Serviços" > "Biblioteca"
   - Pesquise por "Google Sheets API" e ative-a

### 2. Criar Credenciais de Serviço

1. No menu lateral, vá para "APIs e Serviços" > "Credenciais"
2. Clique em "Criar Credenciais" e selecione "Conta de serviço"
3. Preencha os detalhes da conta de serviço e clique em "Criar"
4. Adicione o papel "Editor" à conta de serviço
5. Clique em "Concluído"
6. Na lista de contas de serviço, clique na conta recém-criada
7. Vá para a aba "Chaves" e clique em "Adicionar Chave" > "Criar nova chave"
8. Selecione o formato JSON e clique em "Criar"
9. Salve o arquivo JSON baixado em um local seguro

### 3. Compartilhar a Planilha com a Conta de Serviço

1. Crie uma nova planilha no Google Sheets ou use uma existente
2. Clique no botão "Compartilhar" no canto superior direito
3. Adicione o e-mail da conta de serviço (encontrado no arquivo JSON) com permissão de "Editor"
4. Clique em "Enviar"

### 4. Instalar Dependências Necessárias

```bash
pip install gspread oauth2client
```

### 5. Implementar a Integração

Crie um novo arquivo `sheets_integration.py` no diretório do bot com o seguinte conteúdo:

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# Configuração
CREDENTIALS_FILE = '/caminho/para/seu/arquivo-credenciais.json'
SPREADSHEET_NAME = 'Radar Financeiro - Monitoramento'

class SheetsIntegration:
    def __init__(self, credentials_file=CREDENTIALS_FILE, spreadsheet_name=SPREADSHEET_NAME):
        """Inicializa a integração com o Google Sheets."""
        self.credentials_file = credentials_file
        self.spreadsheet_name = spreadsheet_name
        self.client = None
        self.spreadsheet = None
        
        # Conecta ao Google Sheets
        self.connect()
        
        # Inicializa as planilhas necessárias
        self.init_sheets()
    
    def connect(self):
        """Conecta à API do Google Sheets."""
        try:
            # Define o escopo
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            
            # Autentica com as credenciais
            credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
            self.client = gspread.authorize(credentials)
            
            # Abre a planilha pelo nome
            self.spreadsheet = self.client.open(self.spreadsheet_name)
            
            return True
        except Exception as e:
            print(f"Erro ao conectar ao Google Sheets: {e}")
            return False
    
    def init_sheets(self):
        """Inicializa as planilhas necessárias."""
        try:
            # Lista de planilhas existentes
            existing_sheets = [sheet.title for sheet in self.spreadsheet.worksheets()]
            
            # Cria a planilha de variações se não existir
            if 'Variações' not in existing_sheets:
                variations_sheet = self.spreadsheet.add_worksheet(title='Variações', rows=1000, cols=6)
                # Adiciona cabeçalhos
                variations_sheet.update('A1:F1', [['Data', 'Hora', 'Par', 'Preço', 'Variação (%)', 'Direção']])
                # Formata cabeçalhos
                variations_sheet.format('A1:F1', {'textFormat': {'bold': True}})
            
            # Cria a planilha de notícias se não existir
            if 'Notícias' not in existing_sheets:
                news_sheet = self.spreadsheet.add_worksheet(title='Notícias', rows=1000, cols=7)
                # Adiciona cabeçalhos
                news_sheet.update('A1:G1', [['Data', 'Hora', 'Par', 'Variação (%)', 'Fonte', 'Idioma', 'Conteúdo']])
                # Formata cabeçalhos
                news_sheet.format('A1:G1', {'textFormat': {'bold': True}})
            
            return True
        except Exception as e:
            print(f"Erro ao inicializar planilhas: {e}")
            return False
    
    def add_variation(self, pair, price, variation_pct):
        """Adiciona uma variação de preço à planilha."""
        try:
            # Obtém a planilha de variações
            variations_sheet = self.spreadsheet.worksheet('Variações')
            
            # Prepara os dados
            now = datetime.now()
            date_str = now.strftime('%d/%m/%Y')
            time_str = now.strftime('%H:%M:%S')
            direction = 'Alta' if variation_pct > 0 else 'Queda'
            
            # Adiciona os dados à próxima linha disponível
            next_row = len(variations_sheet.get_all_values()) + 1
            variations_sheet.update(f'A{next_row}:F{next_row}', 
                                   [[date_str, time_str, pair, price, variation_pct, direction]])
            
            return True
        except Exception as e:
            print(f"Erro ao adicionar variação: {e}")
            return False
    
    def add_news(self, pair, variation_pct, news_list):
        """Adiciona notícias à planilha."""
        try:
            # Obtém a planilha de notícias
            news_sheet = self.spreadsheet.worksheet('Notícias')
            
            # Prepara os dados comuns
            now = datetime.now()
            date_str = now.strftime('%d/%m/%Y')
            time_str = now.strftime('%H:%M:%S')
            
            # Adiciona cada notícia à planilha
            for news in news_list:
                # Prepara os dados específicos da notícia
                source = news.get('source', 'Desconhecido')
                language = 'Português' if news.get('language') == 'pt' else 'Inglês'
                content = news.get('content', '')
                if news.get('type') == 'news' and 'title' in news:
                    content = f"{news['title']} - {content}"
                
                # Adiciona os dados à próxima linha disponível
                next_row = len(news_sheet.get_all_values()) + 1
                news_sheet.update(f'A{next_row}:G{next_row}', 
                                 [[date_str, time_str, pair, variation_pct, source, language, content]])
            
            return True
        except Exception as e:
            print(f"Erro ao adicionar notícias: {e}")
            return False

# Exemplo de uso
if __name__ == "__main__":
    integration = SheetsIntegration()
    
    # Testa a adição de uma variação
    integration.add_variation('BTC/USD', 65000.0, 2.5)
    
    # Testa a adição de notícias
    test_news = [
        {
            'type': 'news',
            'language': 'pt',
            'title': 'Bitcoin atinge nova alta',
            'content': 'A criptomoeda atingiu novo patamar após anúncios de grandes investidores.',
            'source': 'Portal Cripto'
        },
        {
            'type': 'tweet',
            'language': 'en',
            'content': 'Breaking: Major institutional investors announce new Bitcoin purchases.',
            'source': '@CryptoNewsDaily'
        }
    ]
    
    integration.add_news('BTC/USD', 2.5, test_news)
```

### 6. Modificar o Bot para Usar a Integração

Adicione o seguinte código ao arquivo `bot.py` para integrar com o Google Sheets:

```python
# Importe a classe SheetsIntegration
from sheets_integration import SheetsIntegration

# Inicialize a integração com o Google Sheets
sheets_integration = None
try:
    sheets_integration = SheetsIntegration()
    logger.info("Integração com Google Sheets inicializada com sucesso")
except Exception as e:
    logger.error(f"Erro ao inicializar integração com Google Sheets: {e}")

# Modifique a função check_prices na classe EnhancedPriceScheduler
async def check_prices(self):
    # ... código existente ...
    
    # Após detectar uma variação significativa e enviar o alerta
    if btc_usd["variation"] is not None and abs(btc_usd["variation"]) >= self.alert_threshold:
        # ... código existente ...
        
        # Registra a variação no Google Sheets
        if sheets_integration:
            try:
                sheets_integration.add_variation("BTC/USD", btc_usd["price"], btc_usd["variation"])
                logger.info(f"Variação de BTC/USD registrada no Google Sheets")
            except Exception as e:
                logger.error(f"Erro ao registrar variação no Google Sheets: {e}")
        
        # Busca e envia notícias relacionadas
        news_list = await send_news_for_alert(self.bot, self.chat_ids, "BTC/USD", btc_usd["variation"])
        
        # Registra as notícias no Google Sheets
        if sheets_integration and news_list:
            try:
                sheets_integration.add_news("BTC/USD", btc_usd["variation"], news_list)
                logger.info(f"Notícias de BTC/USD registradas no Google Sheets")
            except Exception as e:
                logger.error(f"Erro ao registrar notícias no Google Sheets: {e}")
    
    # ... código similar para USD/BRL ...
```

### 7. Testar a Integração

1. Coloque o arquivo de credenciais JSON no diretório do bot
2. Atualize o caminho do arquivo de credenciais no código
3. Execute o bot e verifique se os dados estão sendo registrados na planilha

## Considerações Adicionais

- **Segurança**: Mantenha o arquivo de credenciais seguro e não o compartilhe
- **Limites de API**: A API do Google Sheets tem limites de uso; monitore para evitar exceder
- **Backup**: Implemente um sistema de backup para os dados importantes
- **Formatação**: Considere adicionar formatação condicional na planilha para destacar variações significativas

## Solução de Problemas

- **Erro de Autenticação**: Verifique se o arquivo de credenciais está correto e acessível
- **Erro de Permissão**: Confirme se a conta de serviço tem permissão de edição na planilha
- **Erro de Quota**: Se exceder os limites da API, implemente um sistema de filas ou reduza a frequência de atualizações
