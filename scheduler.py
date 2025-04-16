#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import json
from datetime import datetime
from price_monitor import PriceMonitor

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Diretório para armazenar dados de alertas
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
ALERTS_FILE = os.path.join(DATA_DIR, "alerts.json")

class PriceScheduler:
    def __init__(self, bot=None, chat_ids=None):
        """Inicializa o agendador de verificação de preços."""
        self.monitor = PriceMonitor()
        self.bot = bot
        self.chat_ids = chat_ids or []
        self.alert_threshold = 2.0  # Limiar de alerta em porcentagem
        self.check_interval = 5 * 60  # Intervalo de verificação em segundos (5 minutos)
        self.last_check_time = None
        self.running = False
        
        # Inicializa o arquivo de alertas se não existir
        if not os.path.exists(ALERTS_FILE):
            with open(ALERTS_FILE, 'w') as f:
                json.dump([], f)
    
    def _load_alerts(self):
        """Carrega o histórico de alertas."""
        try:
            with open(ALERTS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logger.warning(f"Erro ao carregar histórico de alertas. Criando novo histórico.")
            return []
    
    def _save_alert(self, pair, variation, price, timestamp):
        """Salva um alerta no histórico."""
        alerts = self._load_alerts()
        
        alerts.append({
            "pair": pair,
            "variation": variation,
            "price": price,
            "timestamp": timestamp,
            "news": []  # Será preenchido posteriormente pela função de busca de notícias
        })
        
        # Limita o histórico a 1000 alertas
        if len(alerts) > 1000:
            alerts = alerts[-1000:]
        
        with open(ALERTS_FILE, 'w') as f:
            json.dump(alerts, f, indent=2)
        
        return len(alerts) - 1  # Retorna o índice do alerta adicionado
    
    async def check_prices(self):
        """Verifica os preços e envia alertas se necessário."""
        logger.info("Verificando preços...")
        self.last_check_time = datetime.now()
        
        # Obtém os dados de preço atuais
        data = self.monitor.get_price_data()
        
        alerts_sent = False
        
        # Verifica BTC/USD
        btc_usd = data["BTC/USD"]
        if btc_usd["variation"] is not None and abs(btc_usd["variation"]) >= self.alert_threshold:
            logger.info(f"Alerta! Variação de {btc_usd['variation']:.2f}% em BTC/USD")
            
            # Salva o alerta
            alert_index = self._save_alert(
                "BTC/USD", 
                btc_usd["variation"], 
                btc_usd["price"], 
                btc_usd["timestamp"]
            )
            
            # Formata a mensagem de alerta
            direction = "aumento" if btc_usd["variation"] > 0 else "queda"
            emoji = "🔺" if btc_usd["variation"] > 0 else "🔻"
            
            message = (
                f"{emoji} ALERTA DE VARIAÇÃO {emoji}\n\n"
                f"Par: BTC/USD\n"
                f"Variação: {btc_usd['variation']:.2f}%\n"
                f"Preço atual: ${btc_usd['price']:,.2f}\n"
                f"Direção: {direction}\n"
                f"Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
                f"Buscando notícias relacionadas..."
            )
            
            # Envia o alerta para todos os chats registrados
            if self.bot and self.chat_ids:
                for chat_id in self.chat_ids:
                    await self.bot.send_message(chat_id=chat_id, text=message)
            
            alerts_sent = True
        
        # Verifica USD/BRL
        usd_brl = data["USD/BRL"]
        if usd_brl["variation"] is not None and abs(usd_brl["variation"]) >= self.alert_threshold:
            logger.info(f"Alerta! Variação de {usd_brl['variation']:.2f}% em USD/BRL")
            
            # Salva o alerta
            alert_index = self._save_alert(
                "USD/BRL", 
                usd_brl["variation"], 
                usd_brl["price"], 
                usd_brl["timestamp"]
            )
            
            # Formata a mensagem de alerta
            direction = "aumento" if usd_brl["variation"] > 0 else "queda"
            emoji = "🔺" if usd_brl["variation"] > 0 else "🔻"
            
            message = (
                f"{emoji} ALERTA DE VARIAÇÃO {emoji}\n\n"
                f"Par: USD/BRL\n"
                f"Variação: {usd_brl['variation']:.2f}%\n"
                f"Preço atual: R${usd_brl['price']:,.2f}\n"
                f"Direção: {direction}\n"
                f"Horário: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n"
                f"Buscando notícias relacionadas..."
            )
            
            # Envia o alerta para todos os chats registrados
            if self.bot and self.chat_ids:
                for chat_id in self.chat_ids:
                    await self.bot.send_message(chat_id=chat_id, text=message)
            
            alerts_sent = True
        
        if not alerts_sent:
            logger.info("Nenhuma variação significativa detectada.")
        
        return data
    
    async def start_monitoring(self):
        """Inicia o monitoramento periódico."""
        self.running = True
        logger.info(f"Iniciando monitoramento a cada {self.check_interval} segundos...")
        
        while self.running:
            try:
                await self.check_prices()
            except Exception as e:
                logger.error(f"Erro durante a verificação de preços: {e}")
            
            # Aguarda o próximo intervalo
            await asyncio.sleep(self.check_interval)
    
    def stop_monitoring(self):
        """Para o monitoramento periódico."""
        self.running = False
        logger.info("Monitoramento interrompido.")
    
    def add_chat_id(self, chat_id):
        """Adiciona um chat ID à lista de destinatários de alertas."""
        if chat_id not in self.chat_ids:
            self.chat_ids.append(chat_id)
            logger.info(f"Chat ID {chat_id} adicionado à lista de alertas.")
    
    def remove_chat_id(self, chat_id):
        """Remove um chat ID da lista de destinatários de alertas."""
        if chat_id in self.chat_ids:
            self.chat_ids.remove(chat_id)
            logger.info(f"Chat ID {chat_id} removido da lista de alertas.")

# Função para teste
if __name__ == "__main__":
    scheduler = PriceScheduler()
    
    async def test():
        await scheduler.check_prices()
    
    asyncio.run(test())
