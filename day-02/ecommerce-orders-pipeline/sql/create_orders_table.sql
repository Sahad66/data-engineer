CREATE TABLE IF NOT EXISTS ecommerce_orders (
    order_id    INTEGER PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    order_date  DATE NOT NULL,
    product     VARCHAR(100) NOT NULL,
    quantity    INTEGER NOT NULL CHECK (quantity > 0),
    unit_price  NUMERIC(10, 2) NOT NULL CHECK (unit_price >= 0),
    status      VARCHAR(20) NOT NULL DEFAULT 'pending'
);    