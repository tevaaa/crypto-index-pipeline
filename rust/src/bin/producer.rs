use anyhow::Result;
use futures_util::StreamExt;
use rdkafka::config::ClientConfig;
use rdkafka::producer::{FutureProducer, FutureRecord};
use rust::config::{KAFKA_BROKER, WSS_URL};
use tokio_tungstenite::{connect_async, tungstenite::Message};

#[tokio::main]
async fn main() -> Result<()> {
    println!("Producer started");

    // producer send message to kafka
    let producer: FutureProducer = ClientConfig::new()
        .set("bootstrap.servers", KAFKA_BROKER)
        .create()?;

    let (stream, _) = connect_async(WSS_URL).await?;
    let (_, mut read) = stream.split();

    while let Some(msg) = read.next().await {
        let msg = msg?;
        println!("Received message: {:?}", msg);
    }

    Ok(())
}
