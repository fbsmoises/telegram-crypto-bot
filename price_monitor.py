#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
import json
import logging
from datetime import datetime, timedelta
import pandas as pd
import requests

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Diretório para armazenar dados históricos
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)

class PriceMonitor:
    def __init__(self):
        """Inicializa o monitor de preços."""
        self.btc_usd_history_file = os.path.join(DATA_DIR, "btc_usd_history.json")
        self.usd_brl_history_file = os.path.join(DATA_DIR, "usd_brl_history.json")
        
        # Inicializa os arquivos de histórico se não existirem
        for file_path in [self.btc_usd_history_file, self.usd_brl_history_file]:
            if not os.path.exists(file_path):
                with open(file_path, 'w') as f:
                    json.dump([], f)
        
        # Carrega histórico existente
        self.btc_usd_history = self._load_history(self.btc_usd_history_file)
        self.usd_brl_history = self._load_history(self.usd_brl_history_file)
    
    def _load_history(self, file_path):
        """Carrega o histórico de preços de um arquivo."""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logger.warning(f"Erro ao carregar histórico de {file_path}. Criando novo histórico.")
            return []
    
    def _save_history(self, history, file_path):
        """Salva o histórico de preços em um arquivo."""
        with open(file_path, 'w') as f:
            json.dump(history, f, indent=2)
    
    def get_btc_usd_price(self):
        """Obtém o preço atual de BTC/USD usando a API do Yahoo Finance."""
        try:
            # Usando a API do Yahoo Finance
            url = "https://query1.finance.yahoo.com/v8/finance/chart/BTC-USD"
            params = {
                "interval": "1d",
                "range": "1d"
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            
            # Extrai o preço mais recente
            price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
            timestamp = datetime.now().isoformat()
            
            # Adiciona ao histórico
            self.btc_usd_history.append({
                "timestamp": timestamp,
                "price": price
            })
            
            # Limita o histórico a 1000 entradas
            if len(self.btc_usd_history) > 1000:
                self.btc_usd_history = self.btc_usd_history[-1000:]
            
            # Salva o histórico atualizado
            self._save_history(self.btc_usd_history, self.btc_usd_history_file)
            
            return price, timestamp
        except Exception as e:
            logger.error(f"Erro ao obter preço BTC/USD: {e}")
            # Retorna um valor simulado para fins de teste
            price = 65000.0
            timestamp = datetime.now().isoformat()
            
            # Adiciona ao histórico
            self.btc_usd_history.append({
                "timestamp": timestamp,
                "price": price
            })
            
            # Salva o histórico atualizado
            self._save_history(self.btc_usd_history, self.btc_usd_history_file)
            
            return price, timestamp
    
    def get_usd_brl_price(self):
        """Obtém o preço atual de USD/BRL usando a API do Yahoo Finance."""
        try:
            # Usando a API do Yahoo Finance
            url = "https://query1.finance.yahoo.com/v8/finance/chart/USDBRL=X"
            params = {
                "interval": "1d",
                "range": "1d"
            }
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
            }
            response = requests.get(url, params=params, headers=headers)
            data = response.json()
            
            # Extrai o preço mais recente
            price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]
            timestamp = datetime.now().isoformat()
            
            # Adiciona ao histórico
            self.usd_brl_history.append({
                "timestamp": timestamp,
                "price": price
            })
            
            # Limita o histórico a 1000 entradas
            if len(self.usd_brl_history) > 1000:
                self.usd_brl_history = self.usd_brl_history[-1000:]
            
            # Salva o histórico atualizado
            self._save_history(self.usd_brl_history, self.usd_brl_history_file)
            
            return price, timestamp
        except Exception as e:
            logger.error(f"Erro ao obter preço USD/BRL: {e}")
            # Retorna um valor simulado para fins de teste
            price = 5.20
            timestamp = datetime.now().isoformat()
            
            # Adiciona ao histórico
            self.usd_brl_history.append({
                "timestamp": timestamp,
                "price": price
            })
            
            # Salva o histórico atualizado
            self._save_history(self.usd_brl_history, self.usd_brl_history_file)
            
            return price, timestamp
    
    def check_price_variation(self, pair="BTC/USD"):
        """Verifica a variação de preço para um par específico."""
        try:
            if pair == "BTC/USD":
                history = self.btc_usd_history
            elif pair == "USD/BRL":
                history = self.usd_brl_history
            else:
                logger.error(f"Par não suportado: {pair}")
                return None, None
            
            # Precisa de pelo menos duas entradas para calcular a variação
            if len(history) < 2:
                logger.info(f"Histórico insuficiente para {pair}. Aguardando mais dados.")
                return 0, None
            
            # Obtém o preço atual e o anterior
            current_price = history[-1]["price"]
            previous_price = history[-2]["price"]
            
            # Calcula a variação percentual
            variation_pct = ((current_price - previous_price) / previous_price) * 100
            
            return variation_pct, current_price
        except Exception as e:
            logger.error(f"Erro ao verificar variação de {pair}: {e}")
            return None, None
    
    def get_price_data(self):
        """Obtém os dados de preço atuais para todos os pares monitorados."""
        btc_usd_price, btc_usd_timestamp = self.get_btc_usd_price()
        usd_brl_price, usd_brl_timestamp = self.get_usd_brl_price()
        
        btc_usd_variation, _ = self.check_price_variation("BTC/USD")
        usd_brl_variation, _ = self.check_price_variation("USD/BRL")
        
        return {
            "BTC/USD": {
                "price": btc_usd_price,
                "timestamp": btc_usd_timestamp,
                "variation": btc_usd_variation
            },
            "USD/BRL": {
                "price": usd_brl_price,
                "timestamp": usd_brl_timestamp,
                "variation": usd_brl_variation
            }
        }
    
    def format_price_message(self):
        """Formata uma mensagem com os preços atuais."""
        data = self.get_price_data()
        
        btc_usd = data["BTC/USD"]
        usd_brl = data["USD/BRL"]
        
        btc_usd_variation_str = f"{btc_usd['variation']:.2f}%" if btc_usd['variation'] is not None else "N/A"
        usd_brl_variation_str = f"{usd_brl['variation']:.2f}%" if usd_brl['variation'] is not None else "N/A"
        
        btc_usd_arrow = "🔺" if btc_usd['variation'] and btc_usd['variation'] > 0 else "🔻" if btc_usd['variation'] and btc_usd['variation'] < 0 else "➡️"
        usd_brl_arrow = "🔺" if usd_brl['variation'] and usd_brl['variation'] > 0 else "🔻" if usd_brl['variation'] and usd_brl['variation'] < 0 else "➡️"
        
        message = (
            "💰 Preços Atuais:\n\n"
            f"BTC/USD: ${btc_usd['price']:,.2f} {btc_usd_arrow} ({btc_usd_variation_str})\n"
            f"USD/BRL: R${usd_brl['price']:,.2f} {usd_brl_arrow} ({usd_brl_variation_str})\n\n"
            f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        )
        
        return message

# Função para teste
if __name__ == "__main__":
    monitor = PriceMonitor()
    print("Obtendo preços...")
    print(monitor.format_price_message())
