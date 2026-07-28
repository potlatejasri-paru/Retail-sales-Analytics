# Power BI Build Guide — Retail Sales Analytics

## 1. Load the data
1. Power BI Desktop → **Get Data → Text/CSV** → `Data/retail_sales_cleaned.csv`.
   *(Alternative: **Get Data → MySQL database** → server `localhost`, database `retail_analytics`, and load the views `v_sales_full`, `v_monthly_trend`, `v_region_perf`, `v_category_perf`.)*
2. In Power Query: set `Order Date` to **Date**, `Sales Amount`/`Profit`/`Unit Price` to **Decimal**, `Discount` to **Percentage**, `Quantity` to **Whole number**.
3. Remove duplicates on `Order ID`, then **Close & Apply**.

## 2. Star schema
| Table | Type | Key columns |
|---|---|---|
| `Fact_Sales` | Fact | Order ID, Customer ID, Product Name, Order Date, Quantity, Unit Price, Discount, Sales Amount, Profit, Payment Method, Salesperson |
| `Dim_Date` | Dimension (DAX `CALENDAR`) | Date, Year, Month No, Month, Year-Month, Quarter |
| `Dim_Customer` | Dimension | Customer ID, Customer Name, Age, Gender |
| `Dim_Product` | Dimension | Product Name, Product Category |
| `Dim_Geography` | Dimension | City, Region |

Relationships: all **one-to-many, single direction** from dimension → `Fact_Sales`.
Mark `Dim_Date` as the official date table.

## 3. Measures
Paste every measure from `DAX_Measures.txt` into a dedicated blank table named `_Measures`.

## 4. Report pages

### Page 1 — Executive Overview
- **KPI cards row (6):** Total Sales, Total Profit, Profit Margin %, Total Orders, Avg Order Value, Total Customers. Use card visuals with the `Margin Colour` measure for conditional font colour on margin.
- **Line chart:** Monthly Sales & Profit Trend — X `Dim_Date[Year-Month]`, Y `[Total Sales]` + `[Total Profit]`, with `[Sales MoM %]` in the tooltip.
- **Bar chart:** Sales by Product Category (horizontal, sorted descending).
- **Donut chart:** Regional share of sales.
- **Map:** Filled/Bubble map on `Dim_Geography[City]`, bubble size `[Total Sales]`, colour saturation `[Profit Margin %]`.
- **Slicers (sync across pages):** Date range slicer, Region, Product Category, Payment Method, Gender.

### Page 2 — Product & Category
- Matrix: Category → Product with Sales, Profit, Margin %, Units (data bars on Sales).
- Top 10 Products bar chart (`Product Rank <= 10` visual-level filter).
- Highest Profit Products bar chart sorted by `[Total Profit]`.
- Scatter: Discount (X) vs Profit Margin % (Y), bubble = Sales, legend = Category.

### Page 3 — Customer & Retention
- Top 10 Customers bar chart (`Customer Rank <= 10`).
- Cards: Repeat Customer Rate %, Customer Lifetime Value, New Customers.
- Cohort matrix: rows = first-purchase month, columns = month offset, values = distinct customers, heat-map background.
- Column charts: Sales by Age Group and by Gender.

### Page 4 — Regional & Sales Team
- Clustered column: Sales vs Profit by Region.
- Map with drill-down Region → City.
- Bar chart: Salesperson performance with `[Sales YoY %]` as a line on a combo chart.
- Table: Region × Category matrix with margin conditional formatting.

## 5. Theme
Save as `Theme.json` (included in this folder) and apply via **View → Themes → Browse for themes**.
- Primary `#1F4E79`, Accent `#2E86AB`, Highlight `#F6A600`, Positive `#27AE60`, Negative `#C0392B`.
- Font: Segoe UI. Card titles 12pt semibold, KPI values 28pt bold.

## 6. Publish
**Home → Publish** to a Power BI workspace, set a scheduled refresh (daily 06:00) and pin the KPI cards to a dashboard.
