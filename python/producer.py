import json
import websocket
from confluent_kafka import Producer
from config import KAFKA_BROKER, KAFKA_TOPIC, ASSETS

producer = Producer({"bootstrap.servers": KAFKA_BROKER})

def on_message(ws, message):
    data = json.loads(message)
    payload = {
        "symbol": data["s"].replace("USDT", ""),
        "price": float(data["c"]),
        "timestamp": data["E"],
    }

    # send to kafka
    producer.produce(KAFKA_TOPIC, json.dumps(payload).encode())
    producer.flush()
    # remove this later
    print(f"{payload['symbol']} → ${payload['price']}")

def on_error(ws, error):
    print(f"Error: {error}")

# streaming 5 assets
streams = "/".join([f"{asset}@ticker" for asset in ASSETS])
url = f"wss://stream.binance.com:9443/ws/{streams}"

ws = websocket.WebSocketApp(url, on_message=on_message, on_error=on_error)
print(f"subscribed to {url}")
ws.run_forever()
