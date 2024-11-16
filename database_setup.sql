-- Create the Shop database
CREATE DATABASE IF NOT EXISTS Shop;

-- Use the Shop database
USE Shop;

-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

-- Create the sales table
CREATE TABLE IF NOT EXISTS sale (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    cust_name VARCHAR(100) NOT NULL,
    sale_date DATE NOT NULL,
    phone VARCHAR(15),
    total_bill DECIMAL(10, 2) NOT NULL
);

-- Create the sales items table (many-to-one relation between products and sales)
CREATE TABLE IF NOT EXISTS sale_items (
    sale_item_id INT AUTO_INCREMENT PRIMARY KEY,
    sale_id INT,
    product_id INT,
    quantity INT NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES sale(sale_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);
