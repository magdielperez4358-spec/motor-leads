#!/usr/bin/env python3
# motormak_daily_auto.py
# Gold Pack Engine - Ejecución diaria automática
# Ultra Productivo | Offline | Multipacks

import os
import json
import csv
import random
from datetime import datetime
import threading
import time

# ---------------- CONFIG ----------------
PACK_DIR = "datasets"
os.makedirs(PACK_DIR, exist_ok=True)

NUM_PACKS = 10         # Packs por ejecución
LEADS_PER_PACK = 500    # Leads por pack
NUM_SAMPLE = 10         # Leads de muestra
RUN_HOUR = 10           # Hora del día para ejecutar automáticamente (24h)

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

    # Archivos
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

    # Checkout simulado
    checkout_url = f"https://simulated.payment/goldpack/{pack_name}"

    # README
    readme_content = f"""
# {pack_name}

**AI-Ready B2B Dataset** - Ultra Productivo Diario

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

Generated automatically by Gold Pack Engine Daily Auto.
"""
    with open(readme_file, "w") as f:
        f.write(readme_content)

    print(f"✅ Pack generado: {pack_name} | Leads: {LEADS_PER_PACK} | Checkout: {checkout_url}")

# ---------------- EJECUTAR MULTIPACK ----------------
def generate_all_packs():
    threads = []
    for i in range(NUM_PACKS):
        t = threading.Thread(target=create_pack, args=(i,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    print(f"\n🚀 {NUM_PACKS} packs generados en total en {PACK_DIR}")

# ---------------- LOOP DIARIO ----------------
while True:
    now = datetime.now()
    if now.hour == RUN_HOUR:
        print(f"\n⏰ Iniciando generación diaria de packs: {now}")
        generate_all_packs()
        # Esperar 1 hora para no repetir en la misma hora
        time.sleep(3600)
    else:
        # Esperar 5 min y revisar la hora de nuevo
        time.sleep(300)
