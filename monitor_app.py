from flask import Flask, jsonify, render_template_string
import psutil, time, random

app = Flask(__name__)
start_time = time.time()

HTML = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lead Intel Console</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #050505; color: #00ff41; font-family: monospace; overflow: hidden; }
        .neon-border { border: 1px solid #00ff41; box-shadow: 0 0 10px #00ff41; }
        .bot-core { animation: pulse 2s infinite; }
        @keyframes pulse { 0% { opacity: 0.5; } 50% { opacity: 1; } 100% { opacity: 0.5; } }
    </style>
</head>
<body class="p-4 flex flex-col h-screen">
    <div class="flex justify-between items-center mb-4 border-b border-green-900 pb-2">
        <h1 class="text-xl font-bold italic">ENGINE_STATUS: ONLINE</h1>
        <div class="text-right text-xs">Uptime: <span id="uptime">0</span>s</div>
    </div>

    <div class="grid grid-cols-2 gap-4 mb-4">
        <div class="neon-border p-2 bg-black bg-opacity-50">
            <p class="text-[10px] text-gray-500">RAM USAGE</p>
            <div id="ram" class="text-2xl">0%</div>
        </div>
        <div class="neon-border p-2 bg-black bg-opacity-50 text-blue-400" style="border-color:#3b82f6; box-shadow: 0 0 10px #3b82f6;">
            <p class="text-[10px] text-gray-400">EST. PROFIT</p>
            <div id="profit" class="text-2xl">/data/data/com.termux/files/usr/bin/bash.00</div>
        </div>
    </div>

    <div class="flex-1 neon-border relative mb-4 bg-black overflow-hidden flex items-center justify-center">
        <div class="absolute inset-0 opacity-20" style="background-image: radial-gradient(#00ff41 1px, transparent 1px); background-size: 20px 20px;"></div>
        <div class="bot-core text-center">
            <div class="text-6xl">🧠</div>
            <p class="text-xs mt-2">BOT_OPERATOR_ACTIVE</p>
        </div>
        <div id="leads-anim" class="absolute text-[10px] text-blue-300"></div>
    </div>

    <div class="h-32 neon-border p-2 bg-black overflow-y-auto text-[10px]" id="logs">
        > Iniciando consola de monitoreo...
    </div>

    <div class="grid grid-cols-3 gap-2 mt-2">
        <button onclick="cmd('restart')" class="bg-red-900 text-white p-2 text-[10px] font-bold">RESTART</button>
        <button onclick="cmd('pause')" class="bg-yellow-900 text-white p-2 text-[10px] font-bold">PAUSE</button>
        <button onclick="location.reload()" class="bg-green-900 text-white p-2 text-[10px] font-bold">REFRESH</button>
    </div>

    <script>
        async function update() {
            const r = await fetch('/system-status');
            const d = await r.json();
            document.getElementById('ram').innerText = d.ram;
            document.getElementById('uptime').innerText = d.uptime;
            document.getElementById('profit').innerText = '$' + (d.uptime * 0.05).toFixed(2);
            const logDiv = document.getElementById('logs');
            logDiv.innerHTML += '<div>[' + new Date().toLocaleTimeString() + '] ' + d.last_log + '</div>';
            logDiv.scrollTop = logDiv.scrollHeight;
        }
        setInterval(update, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML)

@app.route('/system-status')
def status():
    try:
        with open('operador.log', 'r') as f:
            ultimo = f.readlines()[-1].strip()
    except: ultimo = "Reading logs..."
    return jsonify({"ram": f"{psutil.virtual_memory().percent}%", "uptime": int(time.time()-start_time), "last_log": ultimo})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
