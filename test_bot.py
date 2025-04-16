#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
import json
import time
from datetime import datetime

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    filename='/home/ubuntu/telegram_bot/logs/bot.log',
    filemode='a'
)
logger = logging.getLogger(__name__)

# Diretório para logs
LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

def test_price_monitor():
    """Testa o monitor de preços."""
    logger.info("Testando o monitor de preços...")
    
    try:
        from price_monitor import PriceMonitor
        monitor = PriceMonitor()
        
        # Testa a obtenção de preços
        btc_usd_price, btc_usd_timestamp = monitor.get_btc_usd_price()
        usd_brl_price, usd_brl_timestamp = monitor.get_usd_brl_price()
        
        if btc_usd_price and usd_brl_price:
            logger.info(f"BTC/USD: ${btc_usd_price:,.2f} | USD/BRL: R${usd_brl_price:,.2f}")
            print(f"✅ Monitor de preços: OK")
            print(f"   BTC/USD: ${btc_usd_price:,.2f}")
            print(f"   USD/BRL: R${usd_brl_price:,.2f}")
            return True
        else:
            logger.error("Falha ao obter preços")
            print("❌ Monitor de preços: FALHA")
            return False
    
    except Exception as e:
        logger.error(f"Erro ao testar monitor de preços: {e}")
        print(f"❌ Monitor de preços: ERRO - {e}")
        return False

def test_news_searcher():
    """Testa o buscador de notícias."""
    logger.info("Testando o buscador de notícias...")
    
    try:
        from news_searcher import NewsSearcher
        searcher = NewsSearcher()
        
        # Testa a busca de notícias para BTC/USD
        btc_news = searcher.search_news_for_pair("BTC/USD", 2.5)
        
        # Testa a busca de notícias para USD/BRL
        usd_news = searcher.search_news_for_pair("USD/BRL", -1.8)
        
        if btc_news and usd_news:
            logger.info(f"Notícias BTC/USD: {len(btc_news)} | Notícias USD/BRL: {len(usd_news)}")
            print(f"✅ Buscador de notícias: OK")
            print(f"   Notícias BTC/USD: {len(btc_news)} encontradas")
            print(f"   Notícias USD/BRL: {len(usd_news)} encontradas")
            return True
        else:
            logger.error("Falha ao buscar notícias")
            print("❌ Buscador de notícias: FALHA")
            return False
    
    except Exception as e:
        logger.error(f"Erro ao testar buscador de notícias: {e}")
        print(f"❌ Buscador de notícias: ERRO - {e}")
        return False

def test_scheduler():
    """Testa o agendador de verificação de preços."""
    logger.info("Testando o agendador...")
    
    try:
        from scheduler import PriceScheduler
        scheduler = PriceScheduler()
        
        # Verifica se o agendador foi inicializado corretamente
        if scheduler.monitor and scheduler.alert_threshold == 2.0 and scheduler.check_interval == 300:
            logger.info("Agendador inicializado corretamente")
            print(f"✅ Agendador: OK")
            print(f"   Limiar de alerta: {scheduler.alert_threshold}%")
            print(f"   Intervalo de verificação: {scheduler.check_interval // 60} minutos")
            return True
        else:
            logger.error("Falha na inicialização do agendador")
            print("❌ Agendador: FALHA")
            return False
    
    except Exception as e:
        logger.error(f"Erro ao testar agendador: {e}")
        print(f"❌ Agendador: ERRO - {e}")
        return False

def test_bot_structure():
    """Testa a estrutura básica do bot."""
    logger.info("Testando a estrutura do bot...")
    
    try:
        # Verifica se os arquivos principais existem
        files_to_check = [
            "bot.py",
            "price_monitor.py",
            "scheduler.py",
            "news_searcher.py",
            "run_bot.sh",
            "telegrambot.service",
            "install_service.sh"
        ]
        
        missing_files = []
        for file in files_to_check:
            file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
            if not os.path.exists(file_path):
                missing_files.append(file)
        
        if not missing_files:
            logger.info("Todos os arquivos principais encontrados")
            print(f"✅ Estrutura do bot: OK")
            print(f"   Todos os {len(files_to_check)} arquivos principais encontrados")
            return True
        else:
            logger.error(f"Arquivos ausentes: {', '.join(missing_files)}")
            print(f"❌ Estrutura do bot: FALHA - Arquivos ausentes: {', '.join(missing_files)}")
            return False
    
    except Exception as e:
        logger.error(f"Erro ao testar estrutura do bot: {e}")
        print(f"❌ Estrutura do bot: ERRO - {e}")
        return False

def run_tests():
    """Executa todos os testes."""
    print("\n🔍 INICIANDO TESTES DO BOT DO TELEGRAM\n")
    print(f"Data e hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("-" * 50)
    
    # Testa a estrutura do bot
    structure_ok = test_bot_structure()
    
    # Testa o monitor de preços
    price_monitor_ok = test_price_monitor()
    
    # Testa o buscador de notícias
    news_searcher_ok = test_news_searcher()
    
    # Testa o agendador
    scheduler_ok = test_scheduler()
    
    # Resumo dos testes
    print("\n" + "-" * 50)
    print("📊 RESUMO DOS TESTES")
    print("-" * 50)
    
    tests = [
        ("Estrutura do bot", structure_ok),
        ("Monitor de preços", price_monitor_ok),
        ("Buscador de notícias", news_searcher_ok),
        ("Agendador", scheduler_ok)
    ]
    
    all_ok = True
    for name, result in tests:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{name}: {status}")
        all_ok = all_ok and result
    
    print("-" * 50)
    if all_ok:
        print("🎉 TODOS OS TESTES PASSARAM! O bot está pronto para uso.")
    else:
        print("⚠️ ALGUNS TESTES FALHARAM. Verifique os logs para mais detalhes.")
    
    print("\nPara iniciar o bot, execute:")
    print("  ./run_bot.sh")
    print("\nPara instalar como serviço (execução 24/7), execute como root:")
    print("  sudo ./install_service.sh")
    
    # Registra o resultado no log
    logger.info(f"Testes concluídos. Resultado geral: {'SUCESSO' if all_ok else 'FALHA'}")
    
    return all_ok

if __name__ == "__main__":
    run_tests()
