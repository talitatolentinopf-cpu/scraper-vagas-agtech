#!/usr/bin/env python3
import requests
import json
from datetime import datetime
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "")

VAGAS_BASE = [
    {
        "titulo": "Product Technical Specialist (CAN & IoT)",
        "empresa": "Techrx",
        "localizacao": "São Paulo, SP",
        "salario": "R$ 8.000 - 12.000",
        "link": "https://br.linkedin.com/jobs/techrx",
        "plataforma": "LinkedIn",
        "data": datetime.now().isoformat()
    },
    {
        "titulo": "Analista Dev Software Embarcado PL",
        "empresa": "Solinftec",
        "localizacao": "Araçatuba, SP",
        "salario": "R$ 6.000 - 10.000",
        "link": "https://www.solinftec.com.br/careers",
        "plataforma": "Website",
        "data": datetime.now().isoformat()
    },
    {
        "titulo": "Analista Dev Hardware PL",
        "empresa": "Solinftec",
        "localizacao": "Araçatuba, SP",
        "salario": "R$ 6.000 - 10.000",
        "link": "https://www.solinftec.com.br/careers",
        "plataforma": "Website",
        "data": datetime.now().isoformat()
    },
    {
        "titulo": "Analista de Validação Técnica",
        "empresa": "Ituran",
        "localizacao": "São Paulo, SP",
        "salario": "R$ 5.500 - 9.000",
        "link": "https://br.linkedin.com/jobs/ituran",
        "plataforma": "LinkedIn",
        "data": datetime.now().isoformat()
    }
]

def gerar_template(vaga):
    return f"""Olá,

Sou Talita Tolentino, especialista em telemetria e sistemas embarcados com 10+ anos de experiência.

Vi a vaga de {vaga['titulo']} na {vaga['empresa']} e meu background bate perfeitamente:

✓ Profundo conhecimento em CAN bus e protocolos veiculares
✓ Hardware embarcado, DMS e telemetria automotiva
✓ Validação técnica de 4.000 frotas (94,8% redução de risco)
✓ Experiência com Trimble, Maxtrack, Solinftec
✓ Liderança técnica e troubleshooting de sistemas

Gostaria de conversar sobre como posso contribuir para o time.

Fico disponível!

Abraço,
Talita Caroline Tolentino
(19) 99322-7319
talitatolentinopf@gmail.com"""

def enviar_discord(vagas):
    if not DISCORD_WEBHOOK or not vagas:
        return
    
    for vaga in vagas:
        template = gerar_template(vaga)
        
        embed = {
            "title": f"🔍 NOVA VAGA - {vaga['empresa']}",
            "color": 3066993,
            "fields": [
                {"name": "📌 Posição", "value": vaga['titulo'], "inline": False},
                {"name": "📍 Localização", "value": vaga['localizacao'], "inline": True},
                {"name": "💰 Salário", "value": vaga['salario'], "inline": True},
                {"name": "🔗 Link", "value": f"[Clique aqui]({vaga['link']})", "inline": False},
                {"name": "✉️ TEMPLATE PRONTO (copiar e colar no LinkedIn)", "value": f"```{template}```", "inline": False}
            ],
            "footer": {"text": f"📋 {vaga['plataforma']} | {datetime.now().strftime('%d/%m/%Y %H:%M')}"}
        }
        
        payload = {"embeds": [embed], "content": "🚀 **Nova vaga para Talita!**"}
        
        try:
            response = requests.post(DISCORD_WEBHOOK, json=payload, timeout=10)
            if response.status_code == 204:
                print(f"✅ {vaga['empresa']} enviada!")
        except Exception as e:
            print(f"❌ Erro: {e}")

def salvar_historico(vagas):
    try:
        try:
            with open('vagas_historico.json', 'r', encoding='utf-8') as f:
                historico = json.load(f)
        except:
            historico = []
        
        for vaga in vagas:
            if vaga not in historico:
                historico.append(vaga)
        
        with open('vagas_historico.json', 'w', encoding='utf-8') as f:
            json.dump(historico, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Vagas salvas!")
    except Exception as e:
        print(f"⚠️ Erro: {e}")

def main():
    print("\n" + "="*60)
    print("🔍 SCRAPER DE VAGAS")
    print("="*60 + "\n")
    
    vagas = VAGAS_BASE
    print(f"📊 Total: {len(vagas)} vagas\n")
    
    for i, vaga in enumerate(vagas, 1):
        print(f"{i}. {vaga['empresa']} - {vaga['titulo']}")
    
    print("\n📤 Enviando para Discord...")
    enviar_discord(vagas)
    
    print("💾 Salvando histórico...")
    salvar_historico(vagas)
    
    print("\n✅ Pronto!\n")

if __name__ == "__main__":
    main()
