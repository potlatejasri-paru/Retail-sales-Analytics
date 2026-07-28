# Excel Data Cleaning Methodology

**Input:** `Data/retail_sales_raw_uncleaned.csv` (10,120 rows, with deliberate quality issues)
**Output:** `Data/retail_sales_cleaned.csv` + `Retail_Sales_Cleaning_Analysis.xlsx`

| # | Issue | Excel technique | Result |
|---|---|---|---|
| 1 | 120 duplicate order rows | **Data → Remove Duplicates** on `Order ID` | 10,000 unique orders |
| 2 | 100 blank `Quantity` cells | **Go To Special → Blanks**, fill with `1`, then convert to whole number | No nulls |
| 3 | Inconsistent `City` casing | `=PROPER(TRIM(F2))` → paste as values | 20 standard city names |
| 4 | Padded / lowercase `Payment Method` (` upi `) | `=TRIM(PROPER(O2))` + find-and-replace `Upi` → `UPI` | 6 clean categories |
| 5 | `Order Date` stored as text | **Data → Text to Columns → Date (YMD)** | True date type |
| 6 | `Sales Amount` not tied to inputs | Rebuilt as `=J2*I2*(1-K2)` | Auditable measure |
| 7 | Unformatted currency / percent | Number formats `$#,##0.00;($#,##0.00);-` and `0.0%` | Readable output |
| 8 | No summary layer | KPI sheet with `SUM`, `AVERAGE`, `COUNTA`, `SUMPRODUCT(1/COUNTIF())`, plus four pivot-style sheets with native charts | Live dashboard |

## Workbook sheets
| Sheet | Purpose |
|---|---|
| `Cleaning_Log` | Every step with rows affected, raw vs clean row counts |
| `Cleaned_Data` | 10,000 clean records, frozen header, autofilter, formatted |
| `KPI_Dashboard` | 8 KPIs driven entirely by live formulas |
| `Pivot_Category` | Sales/Profit/Margin by category + bar chart |
| `Pivot_Region` | Sales/Profit/Margin by region + pie chart |
| `Pivot_Monthly` | Monthly trend + line chart |
| `Pivot_Payment` | Payment mix + bar chart |
| `Notes` | Conventions: blue = input, black = formula |

## Validation
- Row count reconciles: 10,120 raw → 120 duplicates removed → 10,000 clean.
- `SUM(Sales Amount)` on the clean sheet matches the recalculated formula total.
- Workbook recalculated end-to-end: **0 formula errors** (no `#REF!`, `#DIV/0!`, `#VALUE!`, `#NAME?`).
