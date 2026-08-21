-- ============================================
-- InsightSQL AI Database
-- ============================================

DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS customers;


-- ============================================
-- CUSTOMERS
-- ============================================

CREATE TABLE customers (
    customer_id SERIAL PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    state VARCHAR(100)
);


-- ============================================
-- PRODUCTS
-- ============================================

CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(100),
    price NUMERIC(10,2)
);


-- ============================================
-- ORDERS
-- ============================================

CREATE TABLE orders (
    order_id SERIAL PRIMARY KEY,
    customer_id INT REFERENCES customers(customer_id),
    order_date DATE,
    status VARCHAR(50)
);


-- ============================================
-- ORDER ITEMS
-- ============================================

CREATE TABLE order_items (
    order_item_id SERIAL PRIMARY KEY,
    order_id INT REFERENCES orders(order_id),
    product_id INT REFERENCES products(product_id),
    quantity INT,
    unit_price NUMERIC(10,2)
);


-- ============================================
-- CUSTOMER DATA
-- ============================================

INSERT INTO customers
(customer_name, city, state)
VALUES
('Rahul', 'Ahmedabad', 'Gujarat'),
('Riya', 'Mumbai', 'Maharashtra'),
('Amit', 'Delhi', 'Delhi'),
('Neha', 'Ahmedabad', 'Gujarat'),
('Karan', 'Pune', 'Maharashtra');


-- ============================================
-- PRODUCT DATA
-- ============================================

INSERT INTO products
(product_name, category, price)
VALUES
('Laptop', 'Electronics', 60000),
('Phone', 'Electronics', 30000),
('Headphones', 'Electronics', 3000),
('Keyboard', 'Accessories', 2000),
('Mouse', 'Accessories', 1000);


-- ============================================
-- ORDER DATA
-- ============================================

INSERT INTO orders
(customer_id, order_date, status)
VALUES
(1, '2025-01-10', 'Completed'),
(2, '2025-02-15', 'Completed'),
(3, '2025-03-20', 'Completed'),
(1, '2025-04-05', 'Completed'),
(4, '2025-05-12', 'Completed'),
(5, '2025-06-18', 'Completed');


-- ============================================
-- ORDER ITEM DATA
-- ============================================

INSERT INTO order_items
(order_id, product_id, quantity, unit_price)
VALUES
(1, 1, 1, 60000),
(1, 3, 2, 3000),
(2, 2, 1, 30000),
(2, 5, 2, 1000),
(3, 1, 1, 60000),
(4, 2, 2, 30000),
(5, 4, 3, 2000),
(6, 3, 2, 3000);