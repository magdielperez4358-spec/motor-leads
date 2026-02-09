import os
import json
import random
import subprocess
from datetime import datetime

REPO_PATH = os.path.expanduser("~/motormak")
SAMPLE_SIZE = 10
PAY_LINK = "https://gumroad.com/l/TU_PRODUCTO"

COMPANIES = ["AICorp", "NeuralSoft", "Quantum Labs", "CyberStack"]
INTENTS = ["Hiring SDR", "AI Outreach", "Scaling Sales"]
STATUS = ["Verified", "High Priority"]

def generate_sample(n):
    data = []
    for i in range(n):
        c = random.choice(COMPANIES)
        data.append({
            "company": f"{c}_{i}",
            "email": f"contact{i}@{c.lower()}.com",
            "status": random.choice(STATUS),
            "intent": random.choice(INTENTS)
        })
    return data

def update_repo():
    os.chdir(REPO_PATH)

    today = datetime.now().strftime("%Y-%m-%d")
    filename = f"sample_{today}.json"

    sample = generate_sample(SAMPLE_SIZE)

    # Guardar sample
    with open(filename, "w") as f:
        json.dump(sample, f, indent=2)

    # Actualizar README.md
    readme = f"""
# Free Lead Datasets for AI Training

Daily free dataset sample for AI outreach training.

## Today Sample
File: {filename}

## Download Full Dataset
👉 {PAY_LINK}

Auto-updated by Gold Pack Engine
"""
    with open("README.md", "w") as f:
        f.write(readme)

    # Git add, commit, push
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", f"Auto update {today}"])
    subprocess.run(["git", "push"])

    print("✅ Repo actualizado y subido a GitHub")

# Ejecutar
update_repo()
