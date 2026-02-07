import requests, time, logging

logging.basicConfig(filename='operador.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s', filemode='a')

print("🚀 Operador Iniciado. Generando datos para la App...")

while True:
    try:
        r = requests.get('http://127.0.0.1:8000/batch-process')
        d = r.json()
        log_msg = f"💰 PROFIT: ${d['value_usd']} | LEADS: {d['processed']} | EFF: {d['efficiency']}"
        logging.info(log_msg)
        print(log_msg)
    except Exception as e:
        logging.error(f"ENGINE_OFFLINE")
    time.sleep(8)
