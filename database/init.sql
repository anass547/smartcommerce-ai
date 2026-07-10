-- Schéma initial SmartCommerce AI
-- Basé sur la structure du dataset Olist (adapter selon les besoins)

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR PRIMARY KEY,
    customer_city VARCHAR,
    customer_state VARCHAR
);

CREATE TABLE IF NOT EXISTS products (
    product_id VARCHAR PRIMARY KEY,
    product_category VARCHAR
);

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR REFERENCES customers(customer_id),
    order_status VARCHAR,
    order_purchase_timestamp TIMESTAMP,
    order_delivered_timestamp TIMESTAMP
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id VARCHAR REFERENCES orders(order_id),
    product_id VARCHAR REFERENCES products(product_id),
    price NUMERIC(10, 2),
    freight_value NUMERIC(10, 2),
    PRIMARY KEY (order_id, product_id)
);

CREATE TABLE IF NOT EXISTS payments (
    order_id VARCHAR REFERENCES orders(order_id),
    payment_type VARCHAR,
    payment_value NUMERIC(10, 2)
);

-- Table pour cacher/logguer les anomalies détectées (module 4)
CREATE TABLE IF NOT EXISTS anomalies_log (
    id SERIAL PRIMARY KEY,
    detected_at TIMESTAMP DEFAULT NOW(),
    metric VARCHAR,
    deviation_pct NUMERIC(5, 2),
    message TEXT
);

-- Index utiles pour les agrégations fréquentes
CREATE INDEX IF NOT EXISTS idx_orders_purchase_ts ON orders(order_purchase_timestamp);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
