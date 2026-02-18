use serde::{Deserialize, Serialize};

/// Message format from Binance WebSocket
#[derive(Debug, Deserialize)]
pub struct BinanceMessage {
    pub symbol: String,
    pub price: String,  // Binance give us a String (ex: "123.42")
    pub timestamp: i64, // in ms
}

/// This is the kafka event
#[derive(Debug, Serialize, Deserialize)]
pub struct PriceUpdate {
    pub symbol: String,
    pub price: f64,
    pub timestamp: i64,
}
