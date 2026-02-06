from flask import Flask, request, jsonify
import dns.resolver
import csv
import io
import json

app = Flask(__name__)

DOMINIOS_GRATUITOS = ['gmail.com', 'outlook.com', 'hotmail.com', 'yahoo.com']
KEYWORDS_PODER = ['director', 'ceo', 'owner', 'gerente', 'founder', 'socio']

def validar_dominio_real(email):
    try:
        dominio = email.split('@')[-1]
        registros = dns.resolver.resolve(dominio, 'MX')
        return True if registros else False
    except:
        return False

def analizar_lead(email, cargo):
    email = str(email).lower().strip()
    cargo = str(cargo).lower().strip()
    
    if not validar_dominio_real(email):
        return 0, "Inexistente", "Nulo"

    score = 10
    tipo_email = "Personal"
    dominio = email.split('@')[-1]
    
    if dominio not in DOMINIOS_GRATUITOS:
        score += 50
        tipo_email = "Corporativo"
    
    poder = "Alto" if any(key in cargo for key in KEYWORDS_PODER) else "Bajo"
    if poder == "Alto":
        score += 40
        
    return score, tipo_email, poder

@app.route("/batch-process", methods=["POST"])
def batch_process():
    resultados = []
    
    # Detectar CSV
    if 'file' in request.files:
        file = request.files['file']
        decoded = file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded)
        for row in reader:
            email = row.get("email", "")
            cargo = row.get("cargo", "")
            score, tipo, poder = analizar_lead(email, cargo)
            resultados.append({
                "email": email,
                "score": score,
                "tipo": tipo,
                "poder": poder,
                "prioridad": "ALTA" if score >= 80 else "MEDIA" if score >= 50 else "BAJA"
            })
            
    # Detectar JSON
    elif request.is_json:
        data = request.json.get("leads", [])
        for lead in data:
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
    else:
        return jsonify({"error": "No se envió archivo CSV ni JSON"}), 400
    
    return jsonify({"status": "Success", "processed_count": len(resultados), "data": resultados})

if __name__ == "__main__":
    print("🚀 Motor de Leads listo para pruebas sin pandas")
    app.run(host="0.0.0.0", port=8080)
