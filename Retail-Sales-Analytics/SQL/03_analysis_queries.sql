-- ============================================================
-- 03_analysis_queries.sql : Business analysis (MySQL 8.0+)
-- ============================================================
USE retail_analytics;

-- 1. TOTAL SALES ---------------------------------------------
SELECT ROUND(SUM(sales_amount),2) AS total_sales,
       COUNT(*)                   AS total_orders,
       SUM(quantity)              AS total_units
FROM sales;

-- 2. TOTAL PROFIT --------------------------------------------
SELECT ROUND(SUM(profit),2) AS total_profit,
       ROUND(100*SUM(profit)/SUM(sales_amount),2) AS profit_margin_pct
FROM sales;

-- 3. MONTHLY SALES TREND -------------------------------------
SELECT DATE_FORMAT(order_date,'%Y-%m')            AS month,
       ROUND(SUM(sales_amount),2)                 AS monthly_sales,
       ROUND(SUM(profit),2)                       AS monthly_profit,
       COUNT(*)                                   AS orders,
       ROUND(SUM(sales_amount)
             - LAG(SUM(sales_amount)) OVER (ORDER BY DATE_FORMAT(order_date,'%Y-%m')),2) AS mom_change
FROM sales
GROUP BY month
ORDER BY month;

-- 4. TOP 10 PRODUCTS BY SALES --------------------------------
SELECT product_name, product_category,
       ROUND(SUM(sales_amount),2) AS total_sales,
       SUM(quantity)              AS units_sold
FROM sales
GROUP BY product_name, product_category
ORDER BY total_sales DESC
LIMIT 10;

-- 5. TOP 10 CUSTOMERS ----------------------------------------
SELECT c.customer_id, c.customer_name, c.city, c.region,
       COUNT(*)                   AS orders,
       ROUND(SUM(s.sales_amount),2) AS total_spend,
       ROUND(SUM(s.profit),2)       AS total_profit
FROM sales s JOIN customers c ON c.customer_id = s.customer_id
GROUP BY c.customer_id, c.customer_name, c.city, c.region
ORDER BY total_spend DESC
LIMIT 10;

-- 6. REGIONAL SALES ANALYSIS ---------------------------------
SELECT region,
       ROUND(SUM(sales_amount),2) AS total_sales,
       ROUND(SUM(profit),2)       AS total_profit,
       ROUND(100*SUM(profit)/SUM(sales_amount),2) AS margin_pct,
       COUNT(DISTINCT customer_id) AS customers,
       ROUND(100*SUM(sales_amount)/(SELECT SUM(sales_amount) FROM sales),2) AS pct_of_total
FROM sales
GROUP BY region
ORDER BY total_sales DESC;

-- 7. CATEGORY-WISE SALES -------------------------------------
SELECT product_category,
       ROUND(SUM(sales_amount),2) AS total_sales,
       ROUND(SUM(profit),2)       AS total_profit,
       ROUND(AVG(discount)*100,2) AS avg_discount_pct,
       SUM(quantity)              AS units_sold
FROM sales
GROUP BY product_category
ORDER BY total_sales DESC;

-- 8. AVERAGE ORDER VALUE (overall, monthly, regional) --------
SELECT ROUND(AVG(sales_amount),2) AS avg_order_value FROM sales;

SELECT DATE_FORMAT(order_date,'%Y-%m') AS month,
       ROUND(AVG(sales_amount),2)      AS avg_order_value
FROM sales GROUP BY month ORDER BY month;

SELECT region, ROUND(AVG(sales_amount),2) AS avg_order_value
FROM sales GROUP BY region ORDER BY avg_order_value DESC;

-- 9. HIGHEST PROFIT PRODUCTS ---------------------------------
SELECT product_name, product_category,
       ROUND(SUM(profit),2)        AS total_profit,
       ROUND(100*SUM(profit)/SUM(sales_amount),2) AS margin_pct
FROM sales
GROUP BY product_name, product_category
ORDER BY total_profit DESC
LIMIT 10;

-- 10. CUSTOMER RETENTION ANALYSIS ----------------------------
-- 10a. Repeat vs one-time customers
WITH per_cust AS (
  SELECT customer_id, COUNT(*) AS orders
  FROM sales GROUP BY customer_id
)
SELECT CASE WHEN orders = 1 THEN 'One-time' ELSE 'Repeat' END AS customer_type,
       COUNT(*) AS customers,
       ROUND(100*COUNT(*)/SUM(COUNT(*)) OVER (),2) AS pct
FROM per_cust GROUP BY customer_type;

-- 10b. Monthly cohort retention (months since first purchase)
WITH first_order AS (
  SELECT customer_id, MIN(order_date) AS first_dt FROM sales GROUP BY customer_id
),
activity AS (
  SELECT f.customer_id,
         DATE_FORMAT(f.first_dt,'%Y-%m') AS cohort_month,
         TIMESTAMPDIFF(MONTH, DATE_FORMAT(f.first_dt,'%Y-%m-01'),
                              DATE_FORMAT(s.order_date,'%Y-%m-01')) AS month_offset
  FROM sales s JOIN first_order f ON f.customer_id = s.customer_id
)
SELECT cohort_month, month_offset,
       COUNT(DISTINCT customer_id) AS active_customers
FROM activity
GROUP BY cohort_month, month_offset
ORDER BY cohort_month, month_offset;

-- 10c. RFM-style segmentation
WITH rfm AS (
  SELECT customer_id,
         DATEDIFF((SELECT MAX(order_date) FROM sales), MAX(order_date)) AS recency_days,
         COUNT(*) AS frequency,
         ROUND(SUM(sales_amount),2) AS monetary
  FROM sales GROUP BY customer_id
)
SELECT customer_id, recency_days, frequency, monetary,
       CASE WHEN frequency >= 8 AND recency_days <= 90  THEN 'Champion'
            WHEN frequency >= 4 AND recency_days <= 180 THEN 'Loyal'
            WHEN recency_days > 365                     THEN 'Churned'
            ELSE 'Occasional' END AS segment
FROM rfm ORDER BY monetary DESC;
