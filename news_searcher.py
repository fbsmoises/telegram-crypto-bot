#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import json
import logging
import requests
from datetime import datetime, timedelta

# Configuração de logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Diretório para armazenar dados de notícias
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
NEWS_FILE = os.path.join(DATA_DIR, "news.json")

# Inicializa o arquivo de notícias se não existir
if not os.path.exists(NEWS_FILE):
    with open(NEWS_FILE, 'w') as f:
        json.dump([], f)

class NewsSearcher:
    def __init__(self):
        """Inicializa o buscador de notícias."""
        self.news_cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache válido por 1 hora
    
    def _load_news(self):
        """Carrega o histórico de notícias."""
        try:
            with open(NEWS_FILE, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logger.warning("Erro ao carregar histórico de notícias. Criando novo histórico.")
            return []
    
    def _save_news(self, news_list):
        """Salva o histórico de notícias."""
        with open(NEWS_FILE, 'w') as f:
            json.dump(news_list, f, indent=2)
    
    def _search_twitter(self, query, count=10, lang=None):
        """Busca tweets relacionados ao query."""
        try:
            # Usando a API do Twitter
            url = "https://api.twitter.com/2/search/tweets"
            params = {
                "query": query,
                "count": count,
                "type": "Latest"
            }
            
            if lang:
                params["lang"] = lang
            
            # Simulando a chamada da API do Twitter
            # Em um ambiente real, usaríamos a API do Twitter com autenticação
            # Como estamos usando ferramentas gratuitas, vamos simular os resultados
            
            # Simulação de resultados para BTC/USD
            if "bitcoin" in query.lower() or "btc" in query.lower():
                if lang == "pt":
                    return [
                        {
                            "id": "1",
                            "text": f"Bitcoin atinge nova alta após anúncio de grandes investidores institucionais. #BTC #Crypto",
                            "created_at": datetime.now().isoformat(),
                            "user": {"screen_name": "CriptoNoticiasBR", "name": "Cripto Notícias Brasil"}
                        },
                        {
                            "id": "2",
                            "text": f"Análise técnica: BTC pode testar resistência em $70k nos próximos dias. #Bitcoin #Mercado",
                            "created_at": datetime.now().isoformat(),
                            "user": {"screen_name": "AnalistaCriptoBR", "name": "Analista Cripto"}
                        }
                    ]
                else:  # inglês
                    return [
                        {
                            "id": "3",
                            "text": f"Breaking: Major institutional investors announce new Bitcoin purchases, pushing price up. #BTC #Crypto",
                            "created_at": datetime.now().isoformat(),
                            "user": {"screen_name": "CryptoNewsDaily", "name": "Crypto News Daily"}
                        },
                        {
                            "id": "4",
                            "text": f"Technical analysis: BTC likely to test $70k resistance in coming days. #Bitcoin #Trading",
                            "created_at": datetime.now().isoformat(),
                            "user": {"screen_name": "CryptoAnalyst", "name": "Crypto Market Analyst"}
                        }
                    ]
            
            # Simulação de resultados para USD/BRL
            elif "dolar" in query.lower() or "usd" in query.lower() or "brl" in query.lower():
                if lang == "pt":
                    return [
                        {
                            "id": "5",
                            "text": f"Dólar sobe frente ao real após anúncio de dados econômicos dos EUA. #Dolar #Economia",
                            "created_at": datetime.now().isoformat(),
                            "user": {"screen_name": "EconomiaNews", "name": "Economia News"}
                        },
                        {
                            "id": "6",
                            "text": f"Banco Central intervém no mercado para conter volatilidade do dólar. #BancoCentral #Câmbio",
                            "created_at": datetime.now().isoformat(),
                            "user": {"screen_name": "MercadoFinanceiroBR", "name": "Mercado Financeiro BR"}
                        }
                    ]
                else:  # inglês
                    return [
                        {
                            "id": "7",
                            "text": f"USD strengthens against BRL following US economic data release. #Forex #Trading",
                            "created_at": datetime.now().isoformat(),
                            "user": {"screen_name": "ForexDaily", "name": "Forex Daily News"}
                        },
                        {
                            "id": "8",
                            "text": f"Brazil's Central Bank intervenes to stabilize currency as USD/BRL volatility increases. #EmergingMarkets",
                            "created_at": datetime.now().isoformat(),
                            "user": {"screen_name": "EmergingMarketsNews", "name": "Emerging Markets News"}
                        }
                    ]
            
            # Resultados genéricos
            else:
                if lang == "pt":
                    return [
                        {
                            "id": "9",
                            "text": f"Mercados financeiros voláteis hoje devido a incertezas globais. #Mercados #Investimentos",
                            "created_at": datetime.now().isoformat(),
                            "user": {"screen_name": "FinancasBR", "name": "Finanças Brasil"}
                        }
                    ]
                else:  # inglês
                    return [
                        {
                            "id": "10",
                            "text": f"Financial markets showing volatility due to global uncertainties. #Markets #Investing",
                            "created_at": datetime.now().isoformat(),
                            "user": {"screen_name": "FinanceDaily", "name": "Finance Daily News"}
                        }
                    ]
            
        except Exception as e:
            logger.error(f"Erro ao buscar tweets: {e}")
            return []
    
    def _search_news_api(self, query, language="pt"):
        """Busca notícias relacionadas ao query usando uma API de notícias."""
        try:
            # Simulando a chamada de uma API de notícias gratuita
            # Em um ambiente real, usaríamos uma API como NewsAPI, Gnews, etc.
            # Como estamos usando ferramentas gratuitas, vamos simular os resultados
            
            # Simulação de resultados para BTC/USD
            if "bitcoin" in query.lower() or "btc" in query.lower():
                if language == "pt":
                    return [
                        {
                            "title": "Bitcoin ultrapassa $65 mil após forte demanda institucional",
                            "description": "A criptomoeda atingiu novo patamar após anúncios de grandes investidores.",
                            "url": "https://exemplo.com/noticias/bitcoin-alta",
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Portal Cripto"}
                        },
                        {
                            "title": "Analistas preveem Bitcoin a $100 mil até o final do ano",
                            "description": "Especialistas apontam para tendência de alta sustentada no médio prazo.",
                            "url": "https://exemplo.com/noticias/previsao-bitcoin",
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Economia Digital"}
                        }
                    ]
                else:  # inglês
                    return [
                        {
                            "title": "Bitcoin Surpasses $65K on Strong Institutional Demand",
                            "description": "The cryptocurrency reached new heights following announcements from major investors.",
                            "url": "https://example.com/news/bitcoin-surge",
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Crypto Portal"}
                        },
                        {
                            "title": "Analysts Predict Bitcoin to Reach $100K by Year End",
                            "description": "Experts point to sustained upward trend in the medium term.",
                            "url": "https://example.com/news/bitcoin-prediction",
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Digital Economy"}
                        }
                    ]
            
            # Simulação de resultados para USD/BRL
            elif "dolar" in query.lower() or "usd" in query.lower() or "brl" in query.lower():
                if language == "pt":
                    return [
                        {
                            "title": "Dólar sobe após Fed sinalizar manutenção de juros altos",
                            "description": "A moeda americana se fortaleceu frente ao real após comunicado do banco central americano.",
                            "url": "https://exemplo.com/noticias/dolar-alta",
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Economia Hoje"}
                        },
                        {
                            "title": "BC intervém no mercado de câmbio para conter volatilidade",
                            "description": "Banco Central brasileiro realizou leilões de swap cambial para estabilizar o mercado.",
                            "url": "https://exemplo.com/noticias/bc-intervencao",
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Valor Econômico"}
                        }
                    ]
                else:  # inglês
                    return [
                        {
                            "title": "USD Rises After Fed Signals Continued High Interest Rates",
                            "description": "The American currency strengthened against the Brazilian real following the US central bank statement.",
                            "url": "https://example.com/news/usd-rise",
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Economy Today"}
                        },
                        {
                            "title": "Brazil's Central Bank Intervenes in FX Market to Contain Volatility",
                            "description": "Brazilian Central Bank conducted swap auctions to stabilize the market.",
                            "url": "https://example.com/news/bcb-intervention",
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Economic Value"}
                        }
                    ]
            
            # Resultados genéricos
            else:
                if language == "pt":
                    return [
                        {
                            "title": "Mercados financeiros voláteis devido a tensões geopolíticas",
                            "description": "Incertezas globais afetam negociações em diversas classes de ativos.",
                            "url": "https://exemplo.com/noticias/mercados-volateis",
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Notícias Financeiras"}
                        }
                    ]
                else:  # inglês
                    return [
                        {
                            "title": "Financial Markets Volatile Due to Geopolitical Tensions",
                            "description": "Global uncertainties affect trading across various asset classes.",
                            "url": "https://example.com/news/volatile-markets",
                            "publishedAt": datetime.now().isoformat(),
                            "source": {"name": "Financial News"}
                        }
                    ]
            
        except Exception as e:
            logger.error(f"Erro ao buscar notícias: {e}")
            return []
    
    def search_news_for_pair(self, pair, variation_pct):
        """Busca notícias relacionadas a um par específico e sua variação."""
        logger.info(f"Buscando notícias para {pair} com variação de {variation_pct:.2f}%")
        
        # Define os termos de busca com base no par
        if pair == "BTC/USD":
            query_pt = "Bitcoin BTC criptomoeda preço variação"
            query_en = "Bitcoin BTC cryptocurrency price movement"
        elif pair == "USD/BRL":
            query_pt = "Dólar real câmbio variação economia"
            query_en = "USD BRL exchange rate forex Brazil"
        else:
            logger.error(f"Par não suportado: {pair}")
            return []
        
        # Adiciona termos relacionados à direção da variação
        if variation_pct > 0:
            query_pt += " alta subida aumento"
            query_en += " rise increase surge"
        else:
            query_pt += " queda baixa redução"
            query_en += " fall decrease drop"
        
        # Busca tweets em português e inglês
        tweets_pt = self._search_twitter(query_pt, count=5, lang="pt")
        tweets_en = self._search_twitter(query_en, count=5, lang="en")
        
        # Busca notícias em português e inglês
        news_pt = self._search_news_api(query_pt, language="pt")
        news_en = self._search_news_api(query_en, language="en")
        
        # Combina os resultados
        results = []
        
        # Adiciona tweets em português
        for tweet in tweets_pt:
            results.append({
                "type": "tweet",
                "language": "pt",
                "content": tweet["text"],
                "source": f"@{tweet['user']['screen_name']}",
                "url": f"https://twitter.com/{tweet['user']['screen_name']}/status/{tweet['id']}",
                "timestamp": tweet["created_at"]
            })
        
        # Adiciona tweets em inglês
        for tweet in tweets_en:
            results.append({
                "type": "tweet",
                "language": "en",
                "content": tweet["text"],
                "source": f"@{tweet['user']['screen_name']}",
                "url": f"https://twitter.com/{tweet['user']['screen_name']}/status/{tweet['id']}",
                "timestamp": tweet["created_at"]
            })
        
        # Adiciona notícias em português
        for news in news_pt:
            results.append({
                "type": "news",
                "language": "pt",
                "title": news["title"],
                "content": news["description"],
                "source": news["source"]["name"],
                "url": news["url"],
                "timestamp": news["publishedAt"]
            })
        
        # Adiciona notícias em inglês
        for news in news_en:
            results.append({
                "type": "news",
                "language": "en",
                "title": news["title"],
                "content": news["description"],
                "source": news["source"]["name"],
                "url": news["url"],
                "timestamp": news["publishedAt"]
            })
        
        # Salva os resultados no histórico
        all_news = self._load_news()
        all_news.append({
            "pair": pair,
            "variation": variation_pct,
            "timestamp": datetime.now().isoformat(),
            "results": results
        })
        
        # Limita o histórico a 1000 entradas
        if len(all_news) > 1000:
            all_news = all_news[-1000:]
        
        self._save_news(all_news)
        
        return results
    
    def format_news_message(self, pair, variation_pct, news_list, max_items=5):
        """Formata uma mensagem com as notícias encontradas."""
        if not news_list:
            return f"Não foram encontradas notícias relacionadas à variação de {variation_pct:.2f}% em {pair}."
        
        direction = "alta" if variation_pct > 0 else "queda"
        emoji = "📈" if variation_pct > 0 else "📉"
        
        message = f"{emoji} NOTÍCIAS RELACIONADAS À {direction.upper()} DE {pair} ({variation_pct:.2f}%) {emoji}\n\n"
        
        # Limita o número de itens
        news_list = news_list[:max_items]
        
        # Adiciona as notícias à mensagem
        for i, news in enumerate(news_list, 1):
            lang_emoji = "🇧🇷" if news["language"] == "pt" else "🇺🇸"
            
            if news["type"] == "news":
                message += f"{i}. {lang_emoji} {news['title']}\n"
                message += f"   {news['content']}\n"
                message += f"   Fonte: {news['source']} - {news['url']}\n\n"
            else:  # tweet
                message += f"{i}. {lang_emoji} Tweet de {news['source']}\n"
                message += f"   {news['content']}\n"
                message += f"   {news['url']}\n\n"
        
        message += f"Atualizado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}"
        
        return message

# Função para teste
if __name__ == "__main__":
    searcher = NewsSearcher()
    news = searcher.search_news_for_pair("BTC/USD", 2.5)
    print(searcher.format_news_message("BTC/USD", 2.5, news))
    
    news = searcher.search_news_for_pair("USD/BRL", -1.8)
    print(searcher.format_news_message("USD/BRL", -1.8, news))
