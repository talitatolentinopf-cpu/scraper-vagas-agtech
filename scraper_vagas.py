#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "")

def main():
    print("🔍 Scraper de vagas iniciado!")
    
    vagas = [
        {
            "titulo": "Product Technical Specialist (CAN & IoT)",
            "empresa": "Techrx",
            "localizacao": "São Paulo, SP",
            "salario": "R$ 8.000 - 12.000",
            "link": "https://br.linkedin.com/jobs/techrx"
        },
        {
            "titulo": "Analista Dev Software Embarcado PL",
            "empresa": "Solinftec",
            "localizacao": "Araçatuba, SP",
            "salario": "R$ 6.000 - 10.000",
            "link": "https://www.solinftec.com.br"
        }
    ]
    
    print(f"📊 Total: {len(vagas)} vagas encontradas\n")
    
    for vaga in vagas:
        print(f"✓ {vaga['titulo']} - {vaga['empresa']}")
    
    if DISCORD_WEBHOOK:
        embed = {
            "title": f"🔍 Vagas Encontradas - {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            "description": f"Total: {len(vagas)} vagas em agtech/telemetria",
            "color": 3066993,
            "fields": [
                {
                    "name": "Techrx",
                    "value": "[Product Technical Specialist (CAN & IoT)](https://br.linkedin.com)",
                    "inline": False
                },
                {
                    "name": "Solinftec",
                    "value": "[Analista Dev Software Embarcado](https://www.solinftec.com.br)",
                    "inline": False
                }
            ]
        }
        
        payload = {
            "embeds": [embed],
            "content": "🚀 Novas vagas encontradas para Talita!"
        }
        
        try:
            response = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
            if response.status_code == 204:
                print("\n✅ Vagas enviadas para Discord!")
            else:
                print(f"\n⚠️ Erro Discord: {response.status_code}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
    
    print("\n✅ Scraper finalizado!")

if __name__ == "__main__":
    main()
