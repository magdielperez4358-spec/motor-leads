from flask import Flask, jsonify, render_template_string, request
import psutil, time, os, subprocess

app = Flask(__name__)
start_time = time.time()

HTML_FINAL = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Lead Intelligence Command</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #020202; color: #00ff41; font-family: 'Courier New', monospace; overflow: hidden; }
        .neon-glow { text-shadow: 0 0 10px #00ff41; }
        .orb { animation: pulse 2s infinite; border: 2px solid #00ff41; box-shadow: 0 0 20px #00ff41; }
        @keyframes pulse { 0%, 100% { opacity: 0.5; transform: scale(1); } 50% { opacity: 1; transform: scale(1.05); } }
    </style>
</head>
<body class="h-screen flex flex-col p-4">
    <div class="flex justify-between border-b border-green-900 pb-2 mb-4">
        <h1 class="neon-glow font-bold italic text-sm">AI_CORE_SYSTEM: ACTIVE</h1>
        <div class="text-[10px] text-right">UPTIME: <span id="uptime">0s</span></div>
    </div>

    <div class="flex-1 flex flex-col items-center justify-center border border-green-900 bg-black/60 rounded-lg mb-4 relative">
        <div class="orb w-24 h-24 rounded-full flex items-center justify-center text-4xl bg-black">🧠</div>
        <div class="mt-4 text-[10px] tracking-[0.5em] animate-pulse text-blue-400">ENGINE_RUNNING</div>
    </div>

    <div class="grid grid-cols-2 gap-2 mb-4">
        <div class="bg-black border border-green-900 p-2">
            <p class="text-[8px] opacity-50 uppercase">RAM_VIVO_V40</p>
            <div id="ram" class="text-lg font-bold">0%</div>
        </div>
        <div class="bg-black border border-blue-900 p-2 text-blue-400">
            <p class="text-[8px] opacity-50 uppercase">PROCESS_ID</p>
            <div class="text-lg font-bold">#""" + str(os.getpid()) + """</div>
        </div>
    </div>

    <div id="logs" class="h-32 bg-black border border-green-900 p-2 text-[9px] overflow-y-auto mb-4 font-mono">
        > SYSTEM_READY
    </div>

    <div class="grid grid-cols-3 gap-2">
        <button onclick="exec('restart')" class="bg-red-900 py-3 text-[10px] font-bold rounded">RESTART</button>
        <button onclick="exec('clear')" class="bg-zinc-800 py-3 text-[10px] font-bold rounded">CLEAR_LOG</button>
        <button onclick="location.reload()" class="bg-green-900 py-3 text-[10px] font-bold rounded">REFRESH</button>
    </div>

    <script>
        async function exec(action) {
            const r = await fetch('/control', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: action})
            });
            const d = await r.json();
            alert("COMMAND: " + d.res);
        }

        async function update() {
            try {
                const r = await fetch('/system-status');
                const d = await r.json();
                document.getElementById('ram').innerText = d.ram;
                document.getElementById('uptime').innerText = d.uptime + 's';
                const logDiv = document.getElementById('logs');
                d.logs.forEach(l => {
                    if(!logDiv.innerText.includes(l.substring(0,30))) {
                        logDiv.innerHTML += '<div class="border-l border-green-800 pl-1 mb-1">' + l + '</div>';
                    }
                });
                logDiv.scrollTop = logDiv.scrollHeight;
            } catch(e) {}
        }
        setInterval(update, 2000);
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_FINAL)

@app.route('/system-status')
def status():
    try:
        with open('operador.log', 'r') as f:
            lines = f.readlines()
            last_logs = [l.strip() for l in lines[-5:]] if lines else ["..."]
    except: last_logs = ["Log error"]
    
    return jsonify({
        "ram": f"{psutil.virtual_memory().percent}%",
        "uptime": int(time.time() - start_time),
        "logs": last_logs
    })

@app.route('/control', methods=['POST'])
def control():
    action = request.json.get('action')
    if action == 'restart':
        # Reinicia el operador en segundo plano
        subprocess.Popen(["python", "operador_total.py"])
        return jsonify({"res": "OPERATOR_RESTARTED"})
    if action == 'clear':
        open('operador.log', 'w').close()
        return jsonify({"res": "LOGS_CLEANED"})
    return jsonify({"res": "UNKNOWN"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
