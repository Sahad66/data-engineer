
-- RetailPulse Capstone
-- Phase 2 Part 3: Load CSV files into raw tables

\copy raw.customers (customer_id, customer_name, city) FROM 'E:/study/data enginner/data-engineer-roadmap/capstone-retailpulse/data/raw/customers.csv' WITH (FORMAT CSV, HEADER TRUE);

\copy raw.products (product_id, product_name, category, unit_price) FROM 'E:/study/data enginner/data-engineer-roadmap/capstone-retailpulse/data/raw/products.csv' WITH (FORMAT CSV, HEADER TRUE);

\copy raw.orders (order_id, customer_id, order_date, product_id, quantity) FROM 'E:/study/data enginner/data-engineer-roadmap/capstone-retailpulse/data/raw/orders.csv' WITH (FORMAT CSV, HEADER TRUE);

\copy raw.payments (payment_id, order_id, payment_method, payment_status, amount) FROM 'E:/study/data enginner/data-engineer-roadmap/capstone-retailpulse/data/raw/payments.csv' WITH (FORMAT CSV, HEADER TRUE);
