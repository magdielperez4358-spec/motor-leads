from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# --- Configuración de Leads ---
DOMINIOS_GRATUITOS = ['gmail.com', 'outlook.com', 'hotmail.com']
KEYWORDS_PODER = ['director', 'ceo', 'owner', 'gerente']

def analizar_lead(email, cargo):
    email = str(email).lower().strip()
    cargo = str(cargo).lower().strip()
    score = 10
    tipo_email = "Personal"
    dominio = email.split('@')[-1] if '@' in email else ''

    if dominio and dominio not in DOMINIOS_GRATUITOS:
        score += 50
        tipo_email = "Corporativo"

    poder = "Alto" if any(key in cargo for key in KEYWORDS_PODER) else "Bajo"
    if poder == "Alto":
        score += 40

    return score, tipo_email, poder

@app.route("/batch-process", methods=["POST"])
def batch_process():
    data = request.json or {}
    # Para testing, ignoramos pago
    leads = data.get("leads", [])
    resultados = []

    for lead in leads:
        email = lead.get("email", "")
        cargo = lead.get("cargo", "")
        score, tipo, poder = analizar_lead(email, cargo)
        resultados.append({
            "email": email,
            "score": score,
            "tipo_email": tipo,
            "poder": poder
        })

    return jsonify(resultados), 200

# Endpoint de prueba / salud
@app.route("/")
def health():
    return "OK", 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    print("\n🚀 Motor de Inteligencia de Leads ACTIVO")
    print(f"📡 Puerto: {port} | Endpoint: /batch-process")
    app.run(host="0.0.0.0", port=port)
