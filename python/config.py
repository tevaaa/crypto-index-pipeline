KAFKA_BROKER = "localhost:9092"
KAFKA_TOPIC = "price-updates"

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "crypto_index",
    "user": "pipeline",
    "password": "pipeline",
}

ASSETS = ["btcusdt", "ethusdt", "solusdt", "bnbusdt", "xrpusdt"]

INDEX_WEIGHTS = {
    "BTC": 0.25,
    "ETH": 0.30,
    "SOL": 0.20,
    "XRP": 0.15,
    "BNB": 0.10,
}
