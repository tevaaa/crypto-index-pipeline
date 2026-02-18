use std::collections::HashMap;

pub const WSS_URL: &str = "wss://stream.binance.com:9443/ws/btcusdt@ticker/ethusdt@ticker/solusdt@ticker/bnbusdt@ticker/xrpusdt@ticker";

// ==== KAFKA ====
pub const KAFKA_BROKER: &str = "localhost:9092";
pub const KAFKA_TOPIC: &str = "price-updates";

// ==== ASSETS ====
pub const ASSETS: &[&str] = &["btcusdt", "ethusdt", "solusdt", "bnbusdt", "xrpusdt"];
pub fn index_weights() -> HashMap<String, f64> {
    HashMap::from([
        ("BTC".to_string(), 0.25),
        ("ETH".to_string(), 0.30),
        ("SOL".to_string(), 0.20),
        ("XRP".to_string(), 0.15),
        ("BNB".to_string(), 0.10),
    ])
}

// ==== DATABASE ====
pub const DB_HOST: &str = "localhost";
pub const DB_PORT: u16 = 5432;
pub const DB_NAME: &str = "crypto_index";
pub const DB_USER: &str = "pipeline";
pub const DB_PASSWORD: &str = "pipeline";
