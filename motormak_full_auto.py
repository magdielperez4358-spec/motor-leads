#!/usr/bin/env python3
# motormak_full_auto.py
# Gold Pack Engine Definitivo Todo-en-Uno
# Multipacks diarios, sample, README, Gist publish, offline y listo para API

import os
import csv
import json
import random
from datetime import datetime
import threading
import time
import requests

# ---------------- CONFIG ----------------
PACK_DIR = "datasets"
os.makedirs(PACK_DIR, exist_ok=True)

NUM_PACKS = 10        # Packs por ejecución
LEADS_PER_PACK = 500   # Leads por pack
NUM_SAMPLE = 10        # Leads para sample
RUN_HOUR = 10          # Hora de ejecución automática diaria

# GitHub Gist
GITHUB_TOKEN = "TU_TOKEN_GITHUB"  # Pega tu token
USER = "TU_USUARIO_GITHUB"

COMPANIES = ["AICorp", "NeuralSoft", "Quantum Labs", "DataForge", "CyberStack"]
INTENTS = ["Hiring SDR", "Scaling Sales", "AI Outreach", "Lead Expansion"]
STATUS = ["Verified", "High Priority"]

# ---------------- FUNCIONES ----------------
def generate_leads(n):
    leads = []
    for i in range(n):
        c = random.choice(COMPANIES)
        leads.append({
            "company": f"{c}_{i}",
            "founder": f"Founder_{i}",
            "email": f"contact{i}@{c.lower()}.com",
            "linkedin": f"linkedin.com/in/founder{i}",
            "status": random.choice(STATUS),
            "intent": random.choice(INTENTS)
        })
    return leads

def create_pack(pack_index):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S%f")
    pack_name = f"goldpack_{timestamp}"
    leads = generate_leads(LEADS_PER_PACK)

    csv_file = os.path.join(PACK_DIR, f"{pack_name}.csv")
    jsonl_file = os.path.join(PACK_DIR, f"{pack_name}.jsonl")
    sample_file = os.path.join(PACK_DIR, f"sample_{NUM_SAMPLE}_leads.json")
    readme_file = os.path.join(PACK_DIR, f"README_{pack_name}.md")

    # CSV
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=leads[0].keys())
        writer.writeheader()
        writer.writerows(leads)

    # JSONL
    with open(jsonl_file, "w") as f:
        for entry in leads:
            f.write(json.dumps(entry) + "\n")

    # Sample
    with open(sample_file, "w") as f:
        json.dump(leads[:NUM_SAMPLE], f, indent=2)

    # Simulated checkout
    checkout_url = f"https://simulated.payment/goldpack/{pack_name}"

    # README
    readme_content = f"""
# {pack_name}

**AI-Ready B2B Dataset** - Ultra Productivo Todo-en-Uno

## Files Included
- CSV dataset: {os.path.basename(csv_file)}
- JSONL dataset: {os.path.basename(jsonl_file)}
- Sample preview: {os.path.basename(sample_file)}

## Schema
company
founder
email
linkedin
status
intent

## Sample
See: {os.path.basename(sample_file)}

## Purchase (Simulated)
[{checkout_url}]({checkout_url})

Generated automatically by Gold Pack Engine Full Auto.
"""
    with open(readme_file, "w") as f:
        f.write(readme_content)

    print(f"✅ Pack generado: {pack_name} | Leads: {LEADS_PER_PACK} | Checkout: {checkout_url}")

    # Publicar todo en Gist
    publish_gist(csv_file)
    publish_gist(jsonl_file)
    publish_gist(sample_file)
    publish_gist(readme_file)

def publish_gist(pack_file):
    filename = os.path.basename(pack_file)
    with open(pack_file, "r") as f:
        content = f.read()

    payload = {
        "description": f"Gold Pack Engine - {filename}",
        "public": True,
        "files": { filename: {"content": content} }
    }

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.post("https://api.github.com/gists", headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        gist_url = response.json()["html_url"]
        print(f"✅ Publicado Gist: {gist_url}")
        return gist_url
    else:
        print(f"❌ Error publicando {filename}: {response.status_code} - {response.text}")
        return None

def generate_all_packs():
    threads = []
    for i in range(NUM_PACKS):
        t = threading.Thread(target=create_pack, args=(i,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print(f"\n🚀 {NUM_PACKS} packs generados y publicados en total en {PACK_DIR}")

# ---------------- LOOP DIARIO ----------------
while True:
    now = datetime.now()
    if now.hour == RUN_HOUR:
        print(f"\n⏰ Iniciando ejecución diaria de Gold Pack Engine: {now}")
        generate_all_packs()
        time.sleep(3600)  # Espera 1 hora para no repetir
    else:
        time.sleep(300)   # Revisar cada 5 min
