import os
import socket
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/batch-process')
def home():
    return {"status": "ACTIVO", "engine": "Intelligence Leads"}

def run_server():
    # Prioridad a la variable de entorno de Koyeb
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"

    # Forzar liberación de socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.close()
    except OSError:
        port = 8080  # Fallback automático si el 8000 sigue bloqueado

    print(f"\n🚀 Motor de Inteligencia de Leads ACTIVO")
    print(f"📡 Puerto: {port} | Endpoint: /batch-process")
    
    app.run(host=host, port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_server()
