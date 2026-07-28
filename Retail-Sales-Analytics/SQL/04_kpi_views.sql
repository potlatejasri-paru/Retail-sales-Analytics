-- Reusable views consumed by Power BI (DirectQuery / Import)
USE retail_analytics;

CREATE OR REPLACE VIEW v_kpi_summary AS
SELECT ROUND(SUM(sales_amount),2) AS total_sales,
       ROUND(SUM(profit),2)       AS total_profit,
       COUNT(*)                   AS total_orders,
       COUNT(DISTINCT customer_id) AS total_customers,
       ROUND(AVG(sales_amount),2) AS avg_order_value,
       ROUND(100*SUM(profit)/SUM(sales_amount),2) AS profit_margin_pct
FROM sales;

CREATE OR REPLACE VIEW v_monthly_trend AS
SELECT DATE_FORMAT(order_date,'%Y-%m') AS month,
       SUM(sales_amount) AS sales, SUM(profit) AS profit, COUNT(*) AS orders
FROM sales GROUP BY month;

CREATE OR REPLACE VIEW v_region_perf AS
SELECT region, SUM(sales_amount) AS sales, SUM(profit) AS profit,
       COUNT(DISTINCT customer_id) AS customers
FROM sales GROUP BY region;

CREATE OR REPLACE VIEW v_category_perf AS
SELECT product_category, SUM(sales_amount) AS sales, SUM(profit) AS profit,
       SUM(quantity) AS units
FROM sales GROUP BY product_category;
