import time
import random

print("Motor iniciado...")

while True:
    leads = random.randint(10, 50)
    profit = round(leads * 0.35, 2)
    eff = 94

    print(f"💰 PROFIT: ${profit} | LEADS: {leads} | EFF: {eff}%")
    time.sleep(8)
