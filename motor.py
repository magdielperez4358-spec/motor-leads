from flask import Flask, request, jsonify, abort
import csv

# --- CONFIGURACIÓN DE STRIPE ---
import stripe
@app.route("/")
def health():
    return "OK", 200stripe.api_key = "sk_test_TU_API_KEY_AQUI"  # 🔑 Reemplaza con tu clave real

app = Flask(__name__)

DOMINIOS_GRATUITOS = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com']
KEYWORDS_PODER = ['director', 'ceo', 'owner', 'gerente', 'founder', 'socio']

def analizar_lead(email, cargo):
    email = str(email).lower().strip()
    cargo = str(cargo).lower().strip()
    score = 10@app.route("/")
def health():
    return "OK", 200
    tipo_email = "Personal"
    dominio = email.split('@')[-1] if '@' in email else ""

    if dominio and dominio not in DOMINIOS_GRATUITOS:
        score += 50
        tipo_email = "Corporativo"

    poder = "Alto" if any(key in cargo for key in KEYWORDS_PODER) else "Bajo"
    if poder == "Alto":
        score += 40

    return score, tipo_email, poder

def verificar_pago(payment_intent_id):
    try:
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        return intent.status == 'succeeded'
    except Exception as e:
        print("Error verificando pago:", e)
        return False
@app.route("/")
def health():
    return "OK", 200
@app.route("/batch-process", methods=["POST"])
def batch_process():
    data = request.json
    payment_intent_id = data.get("payment_intent_id")
    if not payment_intent_id or not verificar_pago(payment_intent_id):
        return abort(402, description="Pago no recibido o inválido")

    leads = data.get("leads", [])
    resultados = []

    for lead in leads:
        email = lead.get("email", "")
        cargo = lead.get("cargo", "")
        score, tipo, poder = analizar_lead(email, cargo)
        resultados.append({
            "email": email,
            "score": score,
            "tipo": tipo,
            "poder": poder,
            "prioridad": "ALTA" if score >= 80 else "MEDIA" if score >= 50 else "BAJA"
        })

    with open("leads_procesados.csv", "w", newline="") as f:
        if resultados:
            writer = csv.DictWriter(f, fieldnames=resultados[0].keys())
            writer.writeheader()
            writer.writerows(resultados)

    return jsonify({"status": "Success", "processed_count": len(resultados), "data": resultados})

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("\n🚀 Motor de Inteligencia de Leads ACTIVO")
    print(f"📡 Puerto: {port} | Endpoint: /batch-process")
    app.run(host="0.0.0.0", port=port)
