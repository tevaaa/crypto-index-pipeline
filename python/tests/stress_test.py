import json
import time
import random
from confluent_kafka import Producer
from config import KAFKA_BROKER, KAFKA_TOPIC, INDEX_WEIGHTS

producer = Producer({"bootstrap.servers": KAFKA_BROKER})
symbols = list(INDEX_WEIGHTS.keys())

def run_stress_test(num_messages=10000):
    print(f"Sending {num_messages} messages...")
    start = time.time()
    for i in range(num_messages):
        payload = {
            "symbol": random.choice(symbols),
            "price": random.uniform(1, 70000),
            "timestamp": int(time.time() * 1000),
        }
        producer.produce(KAFKA_TOPIC, json.dumps(payload).encode())
        if i % 1000 == 0:
            producer.flush()
    
    # End
    producer.produce(KAFKA_TOPIC, json.dumps({"symbol": "END", "price": 0, "timestamp": 0}).encode())
    producer.flush()
    elapsed = time.time() - start
    print(f"Producer done: {num_messages} msgs in {elapsed:.3f}s ({num_messages/elapsed:,.0f} msg/s)")

if __name__ == "__main__":
    # for n in [1000, 10000, 50000]:
        run_stress_test(100000)
        print()
