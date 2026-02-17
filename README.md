# Architecture

┌─────────────────────┐
│Binance WebSocket API│
└─────────────────────┘
    │
    │  prix live BTC, ETH, SOL, BNB, XRP
    ▼
┌───────────────┐
│Producer Python│
└───────────────┘
    │
    │  JSON serialize → sendTo Kafka
    ▼
┌────────────────────────────┐
│Kafka Topic: "price-updates"│
└────────────────────────────┘
    │
    ▼
┌───────────────┐
│Consumer Python│
└───────────────┘
    │
    ├── 1. Parse message
    ├── 2. INSERT in "prices" table
    ├── 3. RECALCULATE INDEX: SUM(price × weight)
    ├─ 4. INSERT in "index_values" table
    │
    ▼
┌──────────┐
│PostgreSQL│
└──────────┘
    ├── assets (BTC, ETH, SOL, BNB, XRP)
    ├── prices (prices history)
    ├── indices (index name, ex: "Top 5")
    ├── index_weights (BTC=0.40, ETH=0.25, SOL=0.15, BNB=0.10, XRP=0.10)
    ├── index_values (index price)
    └── base_price (storing the initial prices for performance comparison)

# Benchmark Results

Environment: Arch Linux, Ryzen 7, 32GB RAM, Docker (Kafka + PostgreSQL)

## End-to-End Pipeline (Kafka → Parse → DB Insert → Index Calculation)

- Stats for consuming a kafka stream of x messages, 

| Language | Messages | Time    | Throughput    | Avg latency |
|----------|----------|---------|---------------|-------------|
| Python   | 1,000    | 0.649s  | 1,540 msg/s   |   0.636ms   |
| Python   | 20,000   | 13.214s | 1,514 msg/s   |   0.649ms   |
| Python   | 100,000  | 66.0.28s| 1,514 msg/s   |   0.648ms   |
|          |          |         |               |             |
| Rust     | 1,000    | x.xxs   | xx,xxx msg/s  |             |
| Rust     | 20,000   | x.xxs   | xx,xxx msg/s  |             |
| Rust     | 100,000  | x.xxs   | xx,xxx msg/s  |             |

Consumer could be optimised by updating the DB each 100 messages instead of every messages

