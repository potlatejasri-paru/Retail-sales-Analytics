# Retail Sales Analytics — Project Report

## 1. Objective
Build an end-to-end retail analytics solution that moves raw transactional data through SQL, Excel, Python and Power BI to answer: how much do we sell, where does profit come from, who buys repeatedly, and what should we change.

## 2. Scope
- 10,000 orders, 1,714 customers, 40 products, 8 categories, 5 regions, 24 months (2023–2024).
- Deliverables: dataset, MySQL schema + queries, cleaned Excel workbook, Python EDA with charts, Power BI dashboard specification, business insights.

## 3. Methodology
1. **Data generation** — a synthetic but realistic dataset with seasonality, price bands by category, weighted customer repeat behaviour and discount-driven margin erosion.
2. **SQL layer** — normalised `customers` / `products` / `sales` tables in MySQL 8, a `v_sales_full` join view, four KPI views for BI, and ten analysis queries (window functions, CTEs, cohort logic, RFM segmentation).
3. **Excel layer** — cleaning of a deliberately dirty extract: duplicate removal, missing-value handling, text standardisation, type conversion, recalculated measures; plus a formula-driven KPI sheet and four pivot-style summary sheets with native Excel charts.
4. **Python layer** — Pandas for aggregation and Matplotlib for eight publication-quality charts; exported summary CSVs feed the documentation.
5. **Power BI layer** — star-schema model, 25+ DAX measures including time intelligence and retention, a four-page report specification and a JSON theme.

## 4. Key results
| Metric | Result |
|---|---|
| Total Sales | $4,178,681 |
| Total Profit | $733,594 (17.6% margin) |
| YoY growth | +20.8% |
| Average Order Value | $417.87 |
| Repeat customer rate | 91.2% |
| Top category | Electronics (53.9% of sales) |

Full narrative in `Business_Insights_and_Recommendations.md`.

## 5. Techniques demonstrated
Data modelling · SQL window functions & CTEs · cohort and RFM analysis · Excel data cleaning and dashboarding · Pandas groupby/aggregation pipelines · Matplotlib visual design · DAX time intelligence · KPI storytelling.

## 6. Limitations & next steps
- The dataset is synthetic; distributions are plausible but not observed.
- No cost table — profit is modelled, not derived from a COGS ledger.
- Next: add returns and inventory tables, forecast monthly sales with a time-series model, and automate the CSV → MySQL load with a scheduled Python job.
