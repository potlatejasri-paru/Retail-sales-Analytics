-- ============================================================
-- 01_create_database.sql : Retail Sales Analytics (MySQL 8.0+)
-- ============================================================
DROP DATABASE IF EXISTS retail_analytics;
CREATE DATABASE retail_analytics CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE retail_analytics;

CREATE TABLE customers (
  customer_id   VARCHAR(15)  PRIMARY KEY,
  customer_name VARCHAR(100) NOT NULL,
  age           INT          NOT NULL,
  gender        VARCHAR(10)  NOT NULL,
  city          VARCHAR(60)  NOT NULL,
  region        VARCHAR(20)  NOT NULL
) ENGINE=InnoDB;

CREATE TABLE products (
  product_id       INT AUTO_INCREMENT PRIMARY KEY,
  product_name     VARCHAR(100) NOT NULL,
  product_category VARCHAR(60)  NOT NULL,
  UNIQUE KEY uq_product (product_name, product_category)
) ENGINE=InnoDB;

CREATE TABLE sales (
  order_id       VARCHAR(15) PRIMARY KEY,
  customer_id    VARCHAR(15) NOT NULL,
  product_name   VARCHAR(100) NOT NULL,
  product_category VARCHAR(60) NOT NULL,
  quantity       INT NOT NULL,
  unit_price     DECIMAL(10,2) NOT NULL,
  discount       DECIMAL(5,3)  NOT NULL DEFAULT 0,
  sales_amount   DECIMAL(12,2) NOT NULL,
  profit         DECIMAL(12,2) NOT NULL,
  order_date     DATE NOT NULL,
  payment_method VARCHAR(30) NOT NULL,
  salesperson    VARCHAR(60) NOT NULL,
  region         VARCHAR(20) NOT NULL,
  CONSTRAINT fk_sales_customer FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
) ENGINE=InnoDB;

CREATE INDEX idx_sales_date     ON sales(order_date);
CREATE INDEX idx_sales_region   ON sales(region);
CREATE INDEX idx_sales_category ON sales(product_category);
CREATE INDEX idx_sales_customer ON sales(customer_id);

-- Convenience view joining sales with customer demographics
CREATE OR REPLACE VIEW v_sales_full AS
SELECT s.*, c.customer_name, c.age, c.gender, c.city
FROM sales s JOIN customers c ON c.customer_id = s.customer_id;
