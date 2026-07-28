# Streamlit Dashboard

An interactive, Power BI-free way to explore the retail sales dataset.

## Run it

```bash
cd Streamlit
pip install -r requirements.txt
streamlit run app.py
```

Opens at http://localhost:8501.

## What's inside

| Section | Contents |
|---|---|
| Sidebar | Date range + Region, City, Category, Product, Payment Method, Salesperson, Gender, Age band filters |
| KPI cards | Total Sales, Total Profit, Profit Margin, Orders, AOV, Unique Customers, Units Sold — each with a delta vs the prior comparable period |
| Trend | Monthly sales & profit (dual axis) |
| Mix | Sales by Category, Sales share by Region |
| Rankings | Top 10 Products & Top 10 Customers (toggle Sales / Profit) |
| Margin | Discount band vs profit margin, Payment method split |
| People | Salesperson leaderboard coloured by profit |
| Detail | Filtered record table + CSV download |

Data source: `../Data/retail_sales_cleaned.csv` (cached with `@st.cache_data`).
Colours match `PowerBI/Theme.json` so the two dashboards look like one product.
