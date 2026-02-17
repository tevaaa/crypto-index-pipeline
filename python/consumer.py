import json
from confluent_kafka import Consumer
from datetime import datetime
import time
import psycopg2
from config import KAFKA_BROKER, KAFKA_TOPIC, DB_CONFIG, INDEX_WEIGHTS



# ========= BASE PRICE MANAGEMENT ==========
def load_base_prices():
    cursor.execute(
        "SELECT a.symbol, b.price FROM base_prices b "
        "JOIN assets a ON a.id = b.asset_id"
    )
    return {row[0]: float(row[1]) for row in cursor.fetchall()}

# we need to store base price in DB
# if not, the index price will reset to 1000 if consumer needs to restart
def save_base_price(symbol, price):
    cursor.execute(
        "INSERT INTO base_prices (asset_id, price) "
        "SELECT id, %s FROM assets WHERE symbol = %s "
        "ON CONFLICT (asset_id) DO NOTHING",
        (price, symbol)
    )
    connect.commit()

# initial price
# ==========================================


# ==== NORMALIZE (base 1000) ====
def calculate_index(base_prices, latest_prices, weights):
    index_value = 0
    for symbol, weight in weights.items():
        if symbol in latest_prices and symbol in base_prices:
            # relative performance - ex:
            # if BTC 68000 to 69000: ~ 1.00 → 1.0147
            performance = latest_prices[symbol] / base_prices[symbol]
            index_value += performance * weight
    return index_value * 1000

def process_message(msg):
    data = json.loads(msg.value())
    symbol = data["symbol"]
    price = data["price"]
    # I decided to store the formated timestamp,
    # We could juste store time in ms for performances
    ts = datetime.fromtimestamp(data["timestamp"] / 1000)

    # maybe run this in an external loop for initial base price loading
    # once base_prices fetched we don't need this anymore
    if symbol not in base_prices:
        base_prices[symbol] = price
        save_base_price(symbol, price)
        print(f"Found base price: {symbol} = ${price}")

    # - Insert price
    cursor.execute(
        "INSERT INTO prices (asset_id, price, timestamp) "
        "SELECT id, %s, %s FROM assets WHERE symbol = %s",
        (price, ts, symbol)
    )
    print(f"    {symbol} → ${price} stored")

    # Update cache
    latest_prices[symbol] = price

    # Recalculate index if we have all price
    # Should find a way to skip that check later for performances
    if len(latest_prices) == len(INDEX_WEIGHTS):
        index_value = calculate_index(base_prices, latest_prices, INDEX_WEIGHTS)
        cursor.execute(
            "INSERT INTO index_values (index_id, value, timestamp) "
            "VALUES (1, %s, %s)",
            (index_value, ts)
        )
        print(f"💱 Index = ${index_value:,.2f} at {ts}")

    connect.commit()



if __name__ == "__main__":
    # kafka subscribe
    consumer = Consumer({
        "bootstrap.servers": KAFKA_BROKER,
        "group.id": "index-calculator",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe([KAFKA_TOPIC])

    # Postgre connexion
    connect = psycopg2.connect(**DB_CONFIG)
    cursor = connect.cursor()

    # cache
    latest_prices = {}
    base_prices = load_base_prices()

    print("- - - - - - - - - - - - - - - - - - - - -")
    print("| Consumer started, waiting for messages |")
    print("- - - - - - - - - - - - - - - - - - - - -")
    try:
        msg_count = 0
        total_time = 0
        bench_start = None

        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                print(f"❌ {msg.error()}")
                continue

            # ==== FOR BENCHMARK ====
            # data = json.loads(msg.value())
            # if data["symbol"] == "END":
            #     if bench_start and msg_count > 0:
            #         elapsed = time.time() - bench_start
            #         print(f"\n{'='*50}")
            #         print(f"BENCH: {msg_count} msgs in {elapsed:.3f}s")
            #         print(f"Throughput: {msg_count/elapsed:,.0f} msg/s")
            #         print(f"Avg latency: {total_time/msg_count:.3f}ms")
            #         print(f"{'='*50}")
            #     msg_count = 0
            #     total_time = 0
            #     bench_start = None
            #     continue

            # if bench_start is None:
            #     bench_start = time.time()

            # start = time.time()
            process_message(msg)
            # elapsed_ms = (time.time() - start) * 1000
            # msg_count += 1
            # total_time += elapsed_ms

    finally:
        consumer.close()
        connect.close()
