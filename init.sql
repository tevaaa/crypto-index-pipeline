CREATE TABLE assets (
    id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL UNIQUE
);

CREATE TABLE prices (
    id SERIAL PRIMARY KEY,
    asset_id INT REFERENCES assets(id),
    price DECIMAL(18,8) NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE indices (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE index_weights (
    index_id INT REFERENCES indices(id),
    asset_id INT REFERENCES assets(id),
    weight DECIMAL(5,4) NOT NULL,
    PRIMARY KEY (index_id, asset_id)
);

CREATE TABLE index_values (
    id SERIAL PRIMARY KEY,
    index_id INT REFERENCES indices(id),
    value DECIMAL(18,8) NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE base_prices (
    asset_id INT REFERENCES assets(id) UNIQUE,
    price DECIMAL(18,8) NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

INSERT INTO assets (symbol) VALUES ('BTC'), ('ETH'), ('SOL'), ('XRP'), ('BNB');
INSERT INTO indices (name) VALUES ('Top 5 crypto');
INSERT INTO index_weights (index_id, asset_id, weight) VALUES
    (1, 1, 0.2500),
    (1, 2, 0.3000),
    (1, 3, 0.2000),
    (1, 4, 0.1500),
    (1, 5, 0.1000);
