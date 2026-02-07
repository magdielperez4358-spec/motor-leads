from flask import Flask, jsonify
import random

app = Flask(__name__)

@app.route('/batch-process')
def process():
    encontrados = random.randint(15, 60)
    validos = int(encontrados * 0.8)
    profit = round(validos * 0.35, 2)
    return jsonify({
        "status": "SUCCESS",
        "processed": validos,
        "value_usd": profit,
        "efficiency": "94%"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
