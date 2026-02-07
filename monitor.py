from flask import Flask, jsonify
import psutil, time

app = Flask(__name__)
inicio = time.time()

@app.route('/')
def home():
    return f"<html><body style='background:#0a0a0a;color:#00ff41;font-family:monospace;padding:20px;'><meta http-equiv='refresh' content='2'><h1>[ CORE_MONITOR ]</h1><p>ESTADO: ACTIVO</p><p>RAM: {psutil.virtual_memory().percent}%</p><p>UPTIME: {int(time.time()-inicio)}s</p></body></html>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
