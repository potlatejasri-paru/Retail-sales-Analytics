"""Load the retail sales CSV into the MySQL `retail_analytics` database.

Prereq: run SQL/01_create_database.sql first.
Usage:  python load_to_mysql.py --user root --password secret
"""
import argparse, os
import pandas as pd
import mysql.connector

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(BASE, "Data", "retail_sales_data.csv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--user", default="root")
    ap.add_argument("--password", default="")
    ap.add_argument("--database", default="retail_analytics")
    a = ap.parse_args()

    df = pd.read_csv(CSV)
    conn = mysql.connector.connect(host=a.host, user=a.user,
                                   password=a.password, database=a.database)
    cur = conn.cursor()

    customers = df[["Customer ID", "Customer Name", "Age", "Gender", "City", "Region"]] \
        .drop_duplicates("Customer ID").values.tolist()
    cur.executemany(
        "INSERT IGNORE INTO customers (customer_id,customer_name,age,gender,city,region) "
        "VALUES (%s,%s,%s,%s,%s,%s)", customers)

    products = df[["Product Name", "Product Category"]].drop_duplicates().values.tolist()
    cur.executemany(
        "INSERT IGNORE INTO products (product_name,product_category) VALUES (%s,%s)", products)

    sales = df[["Order ID", "Customer ID", "Product Name", "Product Category", "Quantity",
                "Unit Price", "Discount", "Sales Amount", "Profit", "Order Date",
                "Payment Method", "Salesperson", "Region"]].values.tolist()
    cur.executemany(
        "INSERT IGNORE INTO sales (order_id,customer_id,product_name,product_category,quantity,"
        "unit_price,discount,sales_amount,profit,order_date,payment_method,salesperson,region) "
        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", sales)

    conn.commit()
    print(f"Loaded {len(customers):,} customers, {len(products):,} products, {len(sales):,} sales rows.")
    cur.close(); conn.close()


if __name__ == "__main__":
    main()
