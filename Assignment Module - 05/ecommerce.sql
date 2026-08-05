-- -----------------------------------------------------------------------------
-- Assignment on Module 5 : Ecommerce Backend: PostgreSQL, APIs & Data Modeling
-- -----------------------------------------------------------------------------


-- =============================================================================
-- PART 1 - DATABASE CREATION (Database, All tables, Primary Keys, Foreign Keys)
-- =============================================================================

-----------------------------------
-- DATABASE CREATION (ecommerce_db)
-----------------------------------

CREATE DATABASE ecommerce_db;

-----------------------------------------------------------
-- TABLE CREATION (customers, categories, products, orders)
-----------------------------------------------------------

-- creating customers table
CREATE TABLE customers(
	customer_id INT PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	email VARCHAR(100) UNIQUE,
	phone VARCHAR(20),
	city VARCHAR(50)
);


-- creating categories table
CREATE TABLE categories(
	category_id INT PRIMARY KEY,
	category_name VARCHAR(50)
);


-- creating products table with Primary and Foreign Key
CREATE TABLE products(
	product_id INT PRIMARY KEY,
	product_name VARCHAR(100),
	price DECIMAL(10,2),
	stock INT,
	category_id INT,
	CONSTRAINT fk_categories
	FOREIGN KEY (category_id)
	REFERENCES categories(category_id)
);


-- creating orders table with Primary and Foreign Key
CREATE TABLE orders(
	order_id INT PRIMARY KEY,
	customer_id INT,
	CONSTRAINT fk_customer
	FOREIGN KEY (customer_id)
	REFERENCES customers(customer_id),
	order_date DATE,
	total_amount DECIMAL(10,2)
);



-- ===========================================================================
-- PART 2 : INSERT DATA (into customers, categories, products, orders) table
-- ===========================================================================

-- inserting sample data into customers table
INSERT INTO customers(customer_id, name, email, phone, city)
VALUES
(1, 'Raihan Adeeb', 'raihan.adeeb@gmail.com', '01716159852', 'Dhaka'),
(2, 'Nusrat Khan', 'nusrat.khan@gmail.com', '01302515963', 'Khulna'),
(3, 'Abdul Hakim', 'abdul.hakim@yahoo.com', '01657253641', 'Rajshahi'),
(4, 'Zinia Rahman', 'zinia.rahman@hotmail.com', '01914857496', 'Sylhet'),
(5, 'Shihab Shahriar', 'shihab.shahriar@yahoo.com', '01791235478', 'Rangpur'),
(6, 'Kawsar Ahmed', 'kawsar.ahmed@outlook.com', '01752684953', 'Jessore');


-- inserting sample data into categories table
INSERT INTO categories(category_id, category_name)
VALUES
(1, 'Electronics'),
(2, 'Fashion'),
(3, 'Grocery'),
(4, 'Furniture'),
(5, 'Health');


-- inserting sample data into products table
INSERT INTO products(product_id, product_name, price, stock, category_id)
VALUES
(1, 'Laptop', 100000.00, 10, 1 ),
(2, 'Phone', 50000.00, 15, 1),
(3, 'Saree', 10000.00, 8, 2),
(4, 'Panjabee', 5000.00, 30, 2),
(5, 'Soyabean Oil', 975.00, 50, 3),
(6, 'Rice 25Kg Packet', 2250.00, 35, 3),
(7, 'Chair', 3000.00, 15, 4),
(8, 'Table', 40000.00, 5, 4),
(9, 'Thermo Meter', 250.00, 100, 5),
(10, 'BP Machine', 1500.00, 20, 5),
(11, 'Shirt', 2000.00, 50, 2);


-- inserting sample data into orders table
INSERT INTO orders(order_id, customer_id, order_date, total_amount)
VALUES
(1, 1, '2026-08-05', 25000.00),
(2, 2, '2026-01-25', 30000.00),
(3, 4, '2025-12-31', 10000.00),
(4, 5, '2024-03-18', 100000.00),
(5, 3, '2026-01-01', 50000.00),
(6, 1, '2026-02-15', 18000.00),
(7, 3, '2026-04-19', 10000.00),
(8, 2, '2025-11-16', 1500.00),
(9, 4, '2024-07-31', 9750.00);




-- ===========================================================================
-- PART 3 - UPDATE (product price, customer city, product stock)
-- ===========================================================================

-- updating Product price
UPDATE products
SET price=80000.00
WHERE product_name = 'Laptop';


-- updating Customer city
UPDATE customers
SET city = 'Dhaka'
WHERE customer_id = 5;


-- updating Product Stock
UPDATE products
SET stock = 9
WHERE product_id = 1;




-- ===========================================================================
-- PART 4 - DELETE (One customer, One product)
-- ===========================================================================

-- deleting One customer 
ALTER TABLE orders
DROP CONSTRAINT fk_customer;
DELETE FROM customers
WHERE customer_id = 5;


-- deleting One product
ALTER TABLE products
DROP CONSTRAINT fk_categories;
DELETE FROM products
WHERE product_id = 9;




-- ===========================================================================
-- PART 5 - BASIC QUERIES
-- ===========================================================================


-- 1. SQL queries to Show all customers.
SELECT * FROM customers;


-- 2. SQL queries to Show all products.
SELECT * FROM products;


-- 3. SQL queries to Show products whose price is greater than 1000.
SELECT product_id, product_name, price FROM products
WHERE price > 1000
ORDER BY product_id ASC;


-- 4. SQL queries to Show products whose stock is less than 10. 
SELECT product_id, product_name, stock FROM products
WHERE stock < 10;


-- 5. SQL queries to Show customers from Dhaka. 
SELECT customer_id, name, city FROM customers
WHERE city = 'Dhaka';


-- 6. SQL queries to Sort products by price (Highest to Lowest). 
SELECT product_name, price FROM products
ORDER BY price DESC;


-- 7. SQL queries to Sort customers alphabetically. 
SELECT name FROM customers
ORDER BY name ASC;


-- 8. SQL queries to Show first 5 products.
SELECT product_id, product_name FROM products
WHERE product_id <=5
ORDER BY product_id ASC;


-- 9. SQL queries to Count total customers.
SELECT COUNT(*) As Total_customer
FROM customers;


-- 10. SQL queries to Calculate the average product price.
SELECT AVG(price) AS average_product_price
FROM products;





-- ===========================================================================
-- PART 6 - AGGREGATE FUNCTIONS 
-- ===========================================================================

-- write queries to find Maximum product price
SELECT MAX(price) AS maximum_product_price
FROM products;


-- write queries to find Minimum product price
SELECT MIN(price) AS minimum_product_price
FROM products;


-- write queries to find Total stock
SELECT SUM(stock) AS total_stock
FROM products;


--write queries to find Average stock
SELECT AVG(stock) AS average_stock
FROM products;


--write queries to find Total number of orders
SELECT COUNT(*) AS total_number_of_orders
FROM orders;



-- ===========================================================================
-- PART 7 - JOIN QUERIES 
-- ===========================================================================


-- 1. show customer name and their orders
SELECT c.name, o.order_id, o.order_date
FROM customers AS c
INNER JOIN orders AS o
ON c.customer_id = o.customer_id;


-- 2. show product name with category name
SELECT p.product_name, c.category_name
FROM products AS p
INNER JOIN categories AS c
ON p.category_id = c.category_id;


-- 3. show order details with customer name
SELECT o.order_id, o.order_date, o.total_amount, c.name AS customer_name
FROM customers AS c
RIGHT JOIN orders AS o
ON c.customer_id = o.customer_id;




-- ===========================================================================
-- PART 8 - SEARCH QUERIES 
-- ===========================================================================

-- Find products containing the word "Phone"
SELECT * FROM products
WHERE product_name = 'Phone';


-- Find customers whose name start with "A"
SELECT * FROM customers
WHERE name LIKE 'A%';


-- Find Products priced between 500 and 3000
SELECT product_id, product_name, price FROM products
WHERE price BETWEEN 500 AND 3000
ORDER BY price ASC;





-- ===========================================================================
-- PART 9 - BONUS CHALLANGE 
-- ===========================================================================

-- 1. Which product has the highest price ?
SELECT product_name, price AS highest_price
FROM products
WHERE price = (SELECT MAX(price) FROM products);


-- 2. Which customer placed the largest order ?
SELECT c.name, o.total_amount AS largest_order
FROM customers AS c
INNER JOIN orders AS o
ON c.customer_id = o.customer_id
WHERE o.total_amount = (SELECT MAX(total_amount) FROM orders);


-- 3. How many products belong to each category ?
SELECT c.category_name, COUNT(p.product_id) AS total_products
FROM categories AS c
LEFT JOIN products AS p
ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name;


-- 4. Which category has the most products ?
SELECT c.category_id, c.category_name, COUNT(p.product_id) AS total_products
FROM categories AS c
INNER JOIN products AS p 
ON c.category_id = p.category_id
GROUP BY c.category_id, c.category_name
ORDER BY total_products DESC
LIMIT 1;


-- 5. List all customers who have placed at least one order ?
SELECT c.customer_id, c.name, COUNT(o.order_id) AS total_orders_placed
FROM customers AS c
INNER JOIN orders AS o
ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_orders_placed DESC;








