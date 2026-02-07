import os
import socket
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/batch-process')
def home():
    return jsonify({"status": "ACTIVO", "engine": "Intelligence Leads"})

def run_server():
    # Puerto inyectado por Koyeb o fallback 8000
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"

    # Forzar liberación de socket previo
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.close()
    except OSError:
        print(f"⚠️ Puerto {port} ocupado, usando fallback 8080")
        port = 8080
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.close()
        except OSError:
            print("❌ No se pudo liberar puerto 8080. Abortando.")
            return

    print(f"\n🚀 Motor de Inteligencia de Leads ACTIVO")
    print(f"📡 Puerto: {port} | Endpoint: /batch-process")

    app.run(host=host, port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    run_server()
