# Data Dictionary

**Files:** `Data/retail_sales_data.csv` (master), `Data/retail_sales_raw_uncleaned.csv` (cleaning exercise input), `Data/retail_sales_cleaned.csv` (Excel cleaning output)

| Column | Type | Description | Example |
|---|---|---|---|
| Order ID | String (PK) | Unique order identifier | ORD100000 |
| Customer ID | String (FK) | Links to `customers.customer_id` | CUST1000 |
| Customer Name | String | Full name of the customer | Aarav Sharma |
| Age | Integer | Customer age, 18–69 | 34 |
| Gender | String | Male / Female | Female |
| City | String | Customer city (20 cities) | Bengaluru |
| Product Category | String | One of 8 categories | Electronics |
| Product Name | String | SKU name (40 products) | Laptop |
| Quantity | Integer | Units in the order, 1–6 | 2 |
| Unit Price | Decimal | List price per unit ($) | 899.50 |
| Discount | Decimal | Discount rate 0.00–0.25 | 0.10 |
| Sales Amount | Decimal | Unit Price × Quantity × (1 − Discount) | 1619.10 |
| Profit | Decimal | Net profit after cost and discount effect | 284.96 |
| Order Date | Date | Transaction date, 2023-01-01 → 2024-12-31 | 2024-04-17 |
| Payment Method | String | Credit Card, Debit Card, UPI, Net Banking, Cash on Delivery, Wallet | UPI |
| Salesperson | String | Owning sales rep (10 reps) | Sneha Kulkarni |
| Region | String | North, South, East, West, Central | South |

## Business rules
- `Sales Amount = Unit Price × Quantity × (1 − Discount)`
- `Profit Margin % = Profit / Sales Amount`
- Margin declines as discount rises (discount is applied against gross margin).
- Each `Customer ID` maps to exactly one City and Region.

## Known data quality issues in the raw file (intentional, for the Excel exercise)
- 120 duplicate order rows
- 100 missing `Quantity` values
- 100 lowercase `City` values
- 100 `Payment Method` values with padding/casing issues (` upi `)
