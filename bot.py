#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import logging
import os
import json
from datetime import datetime
from price_monitor import PriceMonitor
from scheduler import PriceScheduler
from news_searcher import NewsSearcher

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Token do bot fornecido pelo usuário
TOKEN = "7939454359:AAG8eKjgg2xDZ1AIZByQp2QHN_jnK5WV-Y8"

# Diretório para armazenar dados
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ALERTS_FILE = os.path.join(DATA_DIR, "alerts.json")

# Inicializa o arquivo de usuários se não existir
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, 'w') as f:
        json.dump([], f)

# Inicializa o monitor de preços, o agendador e o buscador de notícias
price_monitor = PriceMonitor()
news_searcher = NewsSearcher()
scheduler = None

def load_users():
    """Carrega a lista de usuários registrados."""
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        logger.warning("Erro ao carregar usuários. Criando nova lista.")
        return []

def save_user(chat_id, username=None, first_name=None):
    """Salva um usuário na lista de usuários registrados."""
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
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    return True

async def send_news_for_alert(bot, chat_ids, pair, variation_pct):
    """Busca notícias relacionadas a um alerta e envia para os usuários."""
    try:
        # Busca notícias relacionadas
        news_list = news_searcher.search_news_for_pair(pair, variation_pct)
        
        if not news_list:
            message = f"Não foram encontradas notícias relacionadas à variação de {variation_pct:.2f}% em {pair}."
        else:
            message = news_searcher.format_news_message(pair, variation_pct, news_list)
        
        # Envia a mensagem para todos os chats registrados
        for chat_id in chat_ids:
            await bot.send_message(chat_id=chat_id, text=message)
        
        return True
    except Exception as e:
        logger.error(f"Erro ao buscar e enviar notícias: {e}")
        return False

# Comandos básicos
async def start(update, context):
    """Envia uma mensagem quando o comando /start é emitido."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Registra o usuário para receber alertas
    is_new = save_user(chat_id, user.username, user.first_name)
    
    # Adiciona o chat_id ao agendador
    if scheduler:
        scheduler.add_chat_id(chat_id)
    
    welcome_text = (
        f"Olá, {user.first_name}! 👋\n\n"
        f"Bem-vindo ao Radar Financeiro Bot! Estou aqui para monitorar os pares BTC/USD e USD/BRL "
        f"e te alertar sobre variações significativas de preço.\n\n"
    )
    
    if is_new:
        welcome_text += "Você foi registrado para receber alertas de variação de preço. "
    else:
        welcome_text += "Você já está registrado para receber alertas de variação de preço. "
    
    welcome_text += "Use /help para ver a lista de comandos disponíveis."
    
    await update.message.reply_text(welcome_text)

async def help_command(update, context):
    """Envia uma mensagem quando o comando /help é emitido."""
    await update.message.reply_text(
        "Aqui estão os comandos disponíveis:\n\n"
        "/start - Inicia o bot e registra para receber alertas\n"
        "/help - Mostra esta mensagem de ajuda\n"
        "/status - Verifica o status atual do monitoramento\n"
        "/preco - Mostra os preços atuais dos pares monitorados\n"
        "/config - Mostra a configuração atual do bot\n"
        "/parar - Para de receber alertas\n"
        "/continuar - Volta a receber alertas\n\n"
        "Este bot monitora automaticamente os pares BTC/USD e USD/BRL a cada 5 minutos "
        "e envia alertas quando há variação de 2% ou mais, junto com notícias relacionadas."
    )

async def status_command(update, context):
    """Envia o status atual do monitoramento."""
    last_check = "Nunca" if not scheduler or not scheduler.last_check_time else scheduler.last_check_time.strftime('%d/%m/%Y %H:%M:%S')
    
    await update.message.reply_text(
        "🔍 Status do Monitoramento:\n\n"
        f"✅ Bot ativo e funcionando\n"
        f"✅ Monitorando BTC/USD\n"
        f"✅ Monitorando USD/BRL\n"
        f"✅ Verificação a cada 5 minutos\n"
        f"✅ Alertas configurados para variações de 2% ou mais\n"
        f"✅ Busca automática de notícias ativada\n\n"
        f"Última verificação: {last_check}"
    )

async def price_command(update, context):
    """Envia os preços atuais dos pares monitorados."""
    await update.message.reply_text("Obtendo preços atuais... Por favor, aguarde.")
    
    try:
        message = price_monitor.format_price_message()
        await update.message.reply_text(message)
    except Exception as e:
        logger.error(f"Erro ao obter preços: {e}")
        await update.message.reply_text(
            "❌ Erro ao obter preços atuais. Por favor, tente novamente mais tarde."
        )

async def config_command(update, context):
    """Envia a configuração atual do bot."""
    threshold = "2%" if not scheduler else f"{scheduler.alert_threshold}%"
    interval = "5 minutos" if not scheduler else f"{scheduler.check_interval // 60} minutos"
    
    await update.message.reply_text(
        "⚙️ Configuração Atual:\n\n"
        f"Pares monitorados: BTC/USD, USD/BRL\n"
        f"Intervalo de verificação: {interval}\n"
        f"Limiar de alerta: {threshold} de variação\n"
        f"Busca de notícias: Ativada (português e inglês)\n"
        f"Modo de execução: 24/7\n\n"
        f"Integração com Google Sheets: Planejada para implementação futura"
    )

async def stop_alerts(update, context):
    """Para de enviar alertas para o usuário."""
    chat_id = update.effective_chat.id
    
    if scheduler:
        scheduler.remove_chat_id(chat_id)
    
    await update.message.reply_text(
        "🔕 Você não receberá mais alertas de variação de preço.\n\n"
        "Use /continuar para voltar a receber alertas."
    )

async def resume_alerts(update, context):
    """Volta a enviar alertas para o usuário."""
    user = update.effective_user
    chat_id = update.effective_chat.id
    
    # Registra o usuário para receber alertas
    save_user(chat_id, user.username, user.first_name)
    
    # Adiciona o chat_id ao agendador
    if scheduler:
        scheduler.add_chat_id(chat_id)
    
    await update.message.reply_text(
        "🔔 Você voltará a receber alertas de variação de preço.\n\n"
        "Use /parar para parar de receber alertas."
    )

async def unknown_command(update, context):
    """Responde a comandos desconhecidos."""
    await update.message.reply_text(
        "Desculpe, não reconheço esse comando. Use /help para ver a lista de comandos disponíveis."
    )

async def error_handler(update, context):
    """Trata erros ocorridos durante o processamento de updates."""
    logger.error(f"Erro durante o processamento de update: {context.error}")

class EnhancedPriceScheduler(PriceScheduler):
    """Versão aprimorada do PriceScheduler com suporte a notícias."""
    
    async def check_prices(self):
        """Verifica os preços e envia alertas com notícias se necessário."""
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
            
            # Busca e envia notícias relacionadas
            await send_news_for_alert(self.bot, self.chat_ids, "BTC/USD", btc_usd["variation"])
            
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
            
            # Busca e envia notícias relacionadas
            await send_news_for_alert(self.bot, self.chat_ids, "USD/BRL", usd_brl["variation"])
            
            alerts_sent = True
        
        if not alerts_sent:
            logger.info("Nenhuma variação significativa detectada.")
        
        return data

def main():
    """Inicia o bot."""
    global scheduler
    
    # Importações dentro da função para evitar problemas de circular import
    from telegram import Update
    from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
    
    # Cria a aplicação e passa o token do bot
    application = Application.builder().token(TOKEN).build()

    # Adiciona handlers para comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("preco", price_command))
    application.add_handler(CommandHandler("config", config_command))
    application.add_handler(CommandHandler("parar", stop_alerts))
    application.add_handler(CommandHandler("continuar", resume_alerts))
    
    # Handler para comandos desconhecidos
    application.add_handler(MessageHandler(filters.COMMAND, unknown_command))
    
    # Handler para erros
    application.add_error_handler(error_handler)
    
    # Inicializa o agendador com a aplicação
    scheduler = EnhancedPriceScheduler(application.bot, [user["chat_id"] for user in load_users()])
    
    # Inicia o monitoramento em background
    asyncio.create_task(scheduler.start_monitoring())
    
    # Inicia o bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
