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
