import lib.gateway as gateway
import lib.discord as discord
import json
import threading
import time
import random

modules = [
    "events",
    "help",
    "fun",
    "admin",
    "inne",
    "permissions_manager",
    "info",
    "dev"
]

gateway.register_modules(modules, gateway, discord)

def status(ws):
    quotes = open("quotes.txt", "r")
    statuses = quotes.read().splitlines()
    quotes.close()

    while True:
        data = {
            "op": 3,
            "d": {
                "since": None,
                "activities": [
                    {
                        "name": random.choice(statuses),
                        "type": random.choice(list(range(1, 4)) + [5])
                    }
                ],
                "status": "dnd",
                "afk": False
            }
        }
        
        data = json.dumps(data)
        ws.send(data)
        time.sleep(10)

@gateway.event
def ready(ctx):
    threading.Thread(target=status, args=(ctx.data["ws"],)).start()
    print("online")

gateway.run()
