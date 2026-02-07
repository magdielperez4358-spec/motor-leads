import sqlite3, os, psutil
from datetime import datetime
from contextlib import contextmanager

DB_PATH = os.path.join(os.path.dirname(__file__), "telemetry.db")

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=10)
    try: yield conn
    finally: conn.close()

def init_db():
    with get_db() as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS metrics (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, leads_processed INTEGER, revenue_usd REAL, success_rate REAL, mem_usage_mb REAL, status_code TEXT)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_timestamp ON metrics(timestamp)")
        conn.commit()

def log_telemetry(leads, revenue, success_rate, status="OK"):
    try:
        mem = psutil.Process(os.getpid()).memory_info().rss / 1024 / 1024
        with get_db() as conn:
            conn.execute("INSERT INTO metrics (leads_processed, revenue_usd, success_rate, mem_usage_mb, status_code) VALUES (?, ?, ?, ?, ?)", (leads, revenue, success_rate, mem, status))
            conn.commit()
    except: pass

init_db()
