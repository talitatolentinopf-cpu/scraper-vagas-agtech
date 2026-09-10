#!/usr/bin/env python3
"""
Scraper de Vagas em Agtech/Telemetria
Busca em: Catho, Vagas.com, Agrobase
Roda na nuvem (Heroku, Google Cloud, GitHub Actions)
"""

import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
import os
from urllib.parse import urlencode

# ===========================
# CONFIGURAÇÃO
# ===========================

PALAVRAS_CHAVE = [
    "telemetria",
    "iot",
    "agtech",
    "sistemas embarcados",
    "CAN bus",
    "IoT agrícola"
]

LOCALIDADES = [
    "Piracicaba",
    "São Paulo",
    "Araçatuba"
]

SALARIO_MINIMO = 5000

# Discord webhook (para notificações)
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "")

# ===========================
# FUNÇÕES DE SCRAPING
# ===========================

def scrape_catho():
    """Busca vagas em Catho.com.br"""
    vagas = []
    
    for keyword in PALAVRAS_CHAVE:
        try:
            url = f"https://www.catho.com.br/vagas?q={keyword}&l=Piracicaba"
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_cards = soup.find_all('div', attrs={'data-testid': 'job-card'})
            
            for card in job_cards[:5]:
                try:
                    titulo = card.find('a').text.strip() if card.find('a') else "N/A"
                    empresa = card.find(attrs={'data-testid': 'company-name'})
                    empresa = empresa.text.strip() if empresa else "N/A"
                    
                    localizacao = card.find(attrs={'data-testid': 'job-location'})
                    localizacao = localizacao.text.strip() if localizacao else "Piracicaba"
                    
                    link = card.find('a')['href'] if card.find('a') else "#"
                    
                    salario = card.find(attrs={'data-testid': 'job-salary'})
                    salario = salario.text.strip() if salario else "Não informado"
                    
                    if titulo and empresa:
                        vagas.append({
                            "titulo": titulo,
                            "empresa": empresa,
                            "localizacao": localizacao,
                            "salario": salario,
                            "link": link,
                            "plataforma": "Catho",
                            "data_busca": datetime.now().isoformat()
                        })
                except Exception
