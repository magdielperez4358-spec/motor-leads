import time
import requests
import subprocess
import datetime
import logging
from logging.handlers import RotatingFileHandler

API = "http://127.0.0.1:8000/batch-process"
INTERVALO = 60
MAX_FALLOS = 3

fallos = 0
ejecuciones = 0
motor = None

# --- Logging con rotación ---
logger = logging.getLogger("operador")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler("operador.log", maxBytes=500_000, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

def log(msg):
    print(msg)
    logger.info(msg)

def iniciar_motor():
    global motor
    if motor is None or motor.poll() is not None:
        log("🚀 Iniciando motor...")
        motor = subprocess.Popen(["python", "motor.py"])
        time.sleep(3)

def reiniciar_motor():
    global motor
    log("⚠ Reiniciando motor...")
    if motor and motor.poll() is None:
        motor.terminate()
        motor.wait()
    iniciar_motor()

log("🧠 OPERADOR PRODUCCIÓN INICIADO")
iniciar_motor()

while True:
    try:
        inicio = time.time()

        r = requests.get(API, timeout=15)
        duracion = round(time.time() - inicio, 2)

        if r.status_code == 200:
            ejecuciones += 1
            fallos = 0

            try:
                data = r.json()
                leads_ok = data.get("ok", "N/A")
                leads_fail = data.get("fail", "N/A")
            except:
                leads_ok = "?"
                leads_fail = "?"

            log(f"OK #{ejecuciones} | leads_ok={leads_ok} fail={leads_fail} | {duracion}s")

        else:
            fallos += 1
            log(f"HTTP error {r.status_code}")

    except requests.exceptions.ConnectionError:
        fallos += 1
        log("Conexión fallida con motor")

    except Exception as e:
        fallos += 1
        log(f"Error inesperado: {e}")

    if fallos >= MAX_FALLOS:
        reiniciar_motor()
        fallos = 0

    time.sleep(INTERVALO)
