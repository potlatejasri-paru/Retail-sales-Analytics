"""
Retail Sales Analytics - Exploratory Data Analysis
Author: Data Analytics Portfolio Project
Usage:  python eda_retail_sales.py
Outputs: charts in ../Dashboard/charts, summary tables in ../Documentation/
"""
import os
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "Data", "retail_sales_data.csv")
CHARTS = os.path.join(BASE, "Dashboard", "charts")
DOCS = os.path.join(BASE, "Documentation")
os.makedirs(CHARTS, exist_ok=True)

PALETTE = ["#1F4E79", "#2E86AB", "#F6A600", "#C0392B", "#27AE60",
           "#8E44AD", "#16A085", "#D35400"]
plt.rcParams.update({"figure.dpi": 130, "font.family": "DejaVu Sans",
                     "axes.spines.top": False, "axes.spines.right": False,
                     "axes.titlesize": 13, "axes.titleweight": "bold"})


def load() -> pd.DataFrame:
    df = pd.read_csv(DATA, parse_dates=["Order Date"])
    df = df.drop_duplicates(subset="Order ID")
    df = df.dropna(subset=["Quantity", "Sales Amount"])
    df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Year"] = df["Order Date"].dt.year
    df["Margin %"] = df["Profit"] / df["Sales Amount"] * 100
    df["Age Group"] = pd.cut(df["Age"], [17, 25, 35, 45, 55, 70],
                             labels=["18-25", "26-35", "36-45", "46-55", "56-70"])
    return df


def save(fig, name):
    fig.tight_layout()
    fig.savefig(os.path.join(CHARTS, name), bbox_inches="tight")
    plt.close(fig)


def kpis(df):
    k = {
        "Total Sales": df["Sales Amount"].sum(),
        "Total Profit": df["Profit"].sum(),
        "Profit Margin %": df["Profit"].sum() / df["Sales Amount"].sum() * 100,
        "Total Orders": len(df),
        "Unique Customers": df["Customer ID"].nunique(),
        "Average Order Value": df["Sales Amount"].mean(),
        "Units Sold": int(df["Quantity"].sum()),
        "Avg Discount %": df["Discount"].mean() * 100,
    }
    print("\n=== KPI SUMMARY ===")
    for a, b in k.items():
        print(f"{a:22}: {b:,.2f}")
    pd.Series(k).round(2).to_csv(os.path.join(DOCS, "kpi_summary.csv"), header=["value"])
    return k


def chart_monthly(df):
    m = df.groupby("Month").agg(Sales=("Sales Amount", "sum"), Profit=("Profit", "sum"))
    fig, ax = plt.subplots(figsize=(11, 4.5))
    ax.plot(m.index, m["Sales"], marker="o", color=PALETTE[0], lw=2, label="Sales")
    ax.plot(m.index, m["Profit"], marker="s", color=PALETTE[2], lw=2, label="Profit")
    ax.fill_between(m.index, m["Sales"], alpha=.10, color=PALETTE[0])
    ax.set_title("Monthly Sales & Profit Trend")
    ax.set_ylabel("Amount ($)")
    ax.tick_params(axis="x", rotation=60)
    ax.legend(frameon=False)
    save(fig, "01_monthly_trend.png")
    m.round(2).to_csv(os.path.join(DOCS, "monthly_trend.csv"))


def chart_category(df):
    c = df.groupby("Product Category")["Sales Amount"].sum().sort_values()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(c.index, c.values, color=PALETTE[1])
    for i, v in enumerate(c.values):
        ax.text(v, i, f" {v:,.0f}", va="center", fontsize=8)
    ax.set_title("Sales by Product Category")
    ax.set_xlabel("Sales ($)")
    save(fig, "02_category_sales.png")


def chart_region(df):
    r = df.groupby("Region")["Sales Amount"].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ax.pie(r.values, labels=r.index, autopct="%1.1f%%", startangle=110,
           colors=PALETTE[:len(r)], wedgeprops={"width": .45, "edgecolor": "white"})
    ax.set_title("Regional Share of Sales")
    save(fig, "03_region_share.png")


def chart_top_products(df):
    p = df.groupby("Product Name")["Sales Amount"].sum().nlargest(10).sort_values()
    fig, ax = plt.subplots(figsize=(8, 4.8))
    ax.barh(p.index, p.values, color=PALETTE[0])
    ax.set_title("Top 10 Products by Sales")
    ax.set_xlabel("Sales ($)")
    save(fig, "04_top_products.png")


def chart_top_customers(df):
    c = df.groupby(["Customer ID", "Customer Name"])["Sales Amount"].sum().nlargest(10)
    labels = [f"{n} ({i})" for i, n in c.index]
    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.barh(labels[::-1], c.values[::-1], color=PALETTE[4])
    ax.set_title("Top 10 Customers by Spend")
    ax.set_xlabel("Spend ($)")
    save(fig, "05_top_customers.png")


def chart_payment_age(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.3))
    pm = df["Payment Method"].value_counts()
    axes[0].bar(pm.index, pm.values, color=PALETTE[5])
    axes[0].set_title("Orders by Payment Method")
    axes[0].tick_params(axis="x", rotation=30)
    ag = df.groupby("Age Group", observed=True)["Sales Amount"].sum()
    axes[1].bar(ag.index.astype(str), ag.values, color=PALETTE[6])
    axes[1].set_title("Sales by Age Group")
    save(fig, "06_payment_and_age.png")


def chart_discount_profit(df):
    d = df.groupby(df["Discount"].round(2)).agg(
        Margin=("Margin %", "mean"), Sales=("Sales Amount", "sum"))
    fig, ax = plt.subplots(figsize=(7.5, 4.3))
    ax.bar(d.index.astype(str), d["Margin"], color=PALETTE[3])
    ax.set_title("Average Profit Margin by Discount Band")
    ax.set_xlabel("Discount")
    ax.set_ylabel("Avg margin (%)")
    save(fig, "07_discount_vs_margin.png")


def retention(df):
    per = df.groupby("Customer ID")["Order ID"].count()
    repeat = (per > 1).mean() * 100
    print(f"\nRepeat customer rate: {repeat:.1f}%  |  One-time: {100-repeat:.1f}%")
    fig, ax = plt.subplots(figsize=(6, 4.2))
    ax.bar(["One-time", "Repeat"], [(per == 1).sum(), (per > 1).sum()],
           color=[PALETTE[3], PALETTE[4]])
    ax.set_title("Customer Retention: One-time vs Repeat")
    save(fig, "08_retention.png")
    return repeat


def tables(df):
    df.groupby("Product Name").agg(Sales=("Sales Amount", "sum"), Profit=("Profit", "sum")) \
        .nlargest(10, "Sales").round(2).to_csv(os.path.join(DOCS, "top_products.csv"))
    df.groupby(["Customer ID", "Customer Name"]).agg(
        Orders=("Order ID", "count"), Spend=("Sales Amount", "sum")) \
        .nlargest(10, "Spend").round(2).to_csv(os.path.join(DOCS, "top_customers.csv"))
    df.groupby("Region").agg(Sales=("Sales Amount", "sum"), Profit=("Profit", "sum")) \
        .round(2).to_csv(os.path.join(DOCS, "region_summary.csv"))
    df.groupby("Product Category").agg(Sales=("Sales Amount", "sum"), Profit=("Profit", "sum")) \
        .round(2).to_csv(os.path.join(DOCS, "category_summary.csv"))


def main():
    df = load()
    print(f"Loaded {len(df):,} clean records covering "
          f"{df['Order Date'].min():%Y-%m-%d} to {df['Order Date'].max():%Y-%m-%d}")
    kpis(df)
    chart_monthly(df); chart_category(df); chart_region(df)
    chart_top_products(df); chart_top_customers(df)
    chart_payment_age(df); chart_discount_profit(df)
    retention(df); tables(df)
    print(f"\nCharts written to {CHARTS}")


if __name__ == "__main__":
    main()
