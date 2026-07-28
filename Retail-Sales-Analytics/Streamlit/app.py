"""
Retail Sales Analytics - Streamlit Dashboard
Run:  streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

PALETTE = ["#1F4E79", "#2E86AB", "#F6A600", "#C0392B",
           "#27AE60", "#8E44AD", "#16A085", "#D35400"]
NAVY, BLUE, AMBER, RED, GREEN = PALETTE[0], PALETTE[1], PALETTE[2], PALETTE[3], PALETTE[4]

st.set_page_config(page_title="Retail Sales Analytics",
                   page_icon="📊", layout="wide")

st.markdown(
    """
    <style>
      .block-container {padding-top: 2rem; padding-bottom: 3rem;}
      div[data-testid="stMetric"] {
          background:#FFFFFF; border:1px solid #E4E7EB; border-radius:10px;
          padding:14px 16px; box-shadow:0 1px 2px rgba(31,78,121,.06);
      }
      div[data-testid="stMetricLabel"] p {color:#52606D; font-size:.80rem;
          text-transform:uppercase; letter-spacing:.04em;}
      div[data-testid="stMetricValue"] {color:#1F4E79; font-size:1.55rem;}
      h1, h2, h3 {color:#1F4E79;}
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_CANDIDATES = [
    Path(__file__).resolve().parent.parent / "Data" / "retail_sales_cleaned.csv",
    Path(__file__).resolve().parent.parent / "Data" / "retail_sales_data.csv",
    Path("Data/retail_sales_cleaned.csv"),
    Path("retail_sales_cleaned.csv"),
]


@st.cache_data(show_spinner="Loading retail sales data...")
def load_data() -> pd.DataFrame:
    path = next((p for p in DATA_CANDIDATES if p.exists()), None)
    if path is None:
        raise FileNotFoundError(
            "retail_sales_cleaned.csv not found. Expected it in the project's Data/ folder."
        )
    df = pd.read_csv(path, parse_dates=["Order Date"])
    df["Month"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()
    df["Age Band"] = pd.cut(
        df["Age"], bins=[0, 24, 34, 44, 54, 200],
        labels=["18-24", "25-34", "35-44", "45-54", "55+"],
    ).astype(str)
    df["Discount Band"] = pd.cut(
        df["Discount"], bins=[-0.001, 0.0001, 0.05, 0.10, 0.15, 0.20, 1.0],
        labels=["0%", "1-5%", "6-10%", "11-15%", "16-20%", "20%+"],
    ).astype(str)
    return df


def money(v: float) -> str:
    if abs(v) >= 1_000_000:
        return f"${v/1_000_000:,.2f}M"
    if abs(v) >= 1_000:
        return f"${v/1_000:,.1f}K"
    return f"${v:,.0f}"


def kpis(df: pd.DataFrame) -> dict:
    sales = df["Sales Amount"].sum()
    profit = df["Profit"].sum()
    orders = df["Order ID"].nunique()
    return {
        "sales": sales,
        "profit": profit,
        "margin": (profit / sales * 100) if sales else 0.0,
        "orders": orders,
        "aov": (sales / orders) if orders else 0.0,
        "customers": df["Customer ID"].nunique(),
        "units": df["Quantity"].sum(),
    }


def pct_delta(cur: float, prev: float):
    if not prev:
        return None
    return f"{(cur - prev) / abs(prev) * 100:+.1f}% vs prior period"


def style(fig, height=360, legend=True):
    fig.update_layout(
        height=height,
        margin=dict(l=10, r=10, t=48, b=10),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#1F2933", size=12),
        title_font=dict(color=NAVY, size=15),
        showlegend=legend,
        legend=dict(orientation="h", y=-0.18, x=0, title=None),
        hoverlabel=dict(bgcolor="white", bordercolor="#E4E7EB"),
    )
    fig.update_xaxes(showgrid=False, linecolor="#E4E7EB")
    fig.update_yaxes(gridcolor="#EEF1F5", zerolinecolor="#E4E7EB")
    return fig


try:
    data = load_data()
except FileNotFoundError as err:
    st.error(str(err))
    st.stop()

# ---------------------------------------------------------------- sidebar
st.sidebar.title("Filters")
st.sidebar.caption("Every visual below reacts to these selections.")

min_d, max_d = data["Order Date"].min().date(), data["Order Date"].max().date()
date_range = st.sidebar.date_input("Order date range", (min_d, max_d),
                                   min_value=min_d, max_value=max_d)
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_d, end_d = date_range
else:
    start_d, end_d = min_d, max_d


def multi(label, col, expanded_default=None):
    opts = sorted(data[col].dropna().unique().tolist())
    return st.sidebar.multiselect(label, opts, default=expanded_default or [])


f_region = multi("Region", "Region")
f_city = multi("City", "City")
f_cat = multi("Product Category", "Product Category")
f_prod = multi("Product Name", "Product Name")
f_pay = multi("Payment Method", "Payment Method")
f_sales_p = multi("Salesperson", "Salesperson")
f_gender = multi("Gender", "Gender")
f_age = multi("Age band", "Age Band")

if st.sidebar.button("Reset filters", use_container_width=True):
    st.rerun()

mask = (data["Order Date"].dt.date >= start_d) & (data["Order Date"].dt.date <= end_d)
for col, sel in [("Region", f_region), ("City", f_city), ("Product Category", f_cat),
                 ("Product Name", f_prod), ("Payment Method", f_pay),
                 ("Salesperson", f_sales_p), ("Gender", f_gender), ("Age Band", f_age)]:
    if sel:
        mask &= data[col].isin(sel)

df = data[mask]

st.title("Retail Sales Analytics Dashboard")
st.caption(
    f"{len(df):,} of {len(data):,} orders  ·  "
    f"{start_d:%d %b %Y} → {end_d:%d %b %Y}"
)

if df.empty:
    st.warning("No records match the current filters. Widen the date range or clear a few selections.")
    st.stop()

# prior comparable period
span = (pd.Timestamp(end_d) - pd.Timestamp(start_d)).days + 1
prev_end = pd.Timestamp(start_d) - pd.Timedelta(days=1)
prev_start = prev_end - pd.Timedelta(days=span - 1)
prev_mask = (data["Order Date"] >= prev_start) & (data["Order Date"] <= prev_end)
for col, sel in [("Region", f_region), ("City", f_city), ("Product Category", f_cat),
                 ("Product Name", f_prod), ("Payment Method", f_pay),
                 ("Salesperson", f_sales_p), ("Gender", f_gender), ("Age Band", f_age)]:
    if sel:
        prev_mask &= data[col].isin(sel)
prev = data[prev_mask]

k, kp = kpis(df), kpis(prev) if not prev.empty else None

c = st.columns(4)
c[0].metric("Total Sales", money(k["sales"]), kp and pct_delta(k["sales"], kp["sales"]))
c[1].metric("Total Profit", money(k["profit"]), kp and pct_delta(k["profit"], kp["profit"]))
c[2].metric("Profit Margin", f"{k['margin']:.1f}%",
            kp and f"{k['margin'] - kp['margin']:+.1f} pts vs prior period")
c[3].metric("Orders", f"{k['orders']:,}", kp and pct_delta(k["orders"], kp["orders"]))

c = st.columns(3)
c[0].metric("Average Order Value", f"${k['aov']:,.2f}", kp and pct_delta(k["aov"], kp["aov"]))
c[1].metric("Unique Customers", f"{k['customers']:,}",
            kp and pct_delta(k["customers"], kp["customers"]))
c[2].metric("Units Sold", f"{int(k['units']):,}", kp and pct_delta(k["units"], kp["units"]))

st.divider()

# ------------------------------------------------------------ trend
monthly = (df.groupby("Month", as_index=False)
             .agg(Sales=("Sales Amount", "sum"), Profit=("Profit", "sum")))
fig = go.Figure()
fig.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Sales"], name="Sales",
                         mode="lines+markers", line=dict(color=NAVY, width=3),
                         fill="tozeroy", fillcolor="rgba(31,78,121,.08)"))
fig.add_trace(go.Scatter(x=monthly["Month"], y=monthly["Profit"], name="Profit",
                         mode="lines+markers", line=dict(color=AMBER, width=3),
                         yaxis="y2"))
fig.update_layout(title="Monthly Sales & Profit Trend",
                  yaxis=dict(title="Sales ($)"),
                  yaxis2=dict(title="Profit ($)", overlaying="y", side="right",
                              showgrid=False))
st.plotly_chart(style(fig, 400), use_container_width=True)

# ------------------------------------------------- category / region
left, right = st.columns((3, 2))
cat = (df.groupby("Product Category", as_index=False)["Sales Amount"].sum()
         .sort_values("Sales Amount"))
f1 = px.bar(cat, x="Sales Amount", y="Product Category", orientation="h",
            title="Sales by Product Category", text_auto=".2s",
            color_discrete_sequence=[BLUE])
f1.update_traces(textposition="outside", cliponaxis=False)
left.plotly_chart(style(f1, 380, legend=False), use_container_width=True)

reg = df.groupby("Region", as_index=False)["Sales Amount"].sum()
f2 = px.pie(reg, names="Region", values="Sales Amount", hole=0.55,
            title="Sales Share by Region", color_discrete_sequence=PALETTE)
f2.update_traces(textinfo="percent+label", textfont_size=11)
right.plotly_chart(style(f2, 380), use_container_width=True)

# --------------------------------------------------------- top 10s
st.subheader("Top performers")
metric = st.radio("Rank by", ["Sales Amount", "Profit"], horizontal=True,
                  label_visibility="collapsed")
left, right = st.columns(2)
top_p = (df.groupby("Product Name", as_index=False)[metric].sum()
           .nlargest(10, metric).sort_values(metric))
f3 = px.bar(top_p, x=metric, y="Product Name", orientation="h",
            title=f"Top 10 Products by {metric}", text_auto=".2s",
            color_discrete_sequence=[NAVY])
f3.update_traces(textposition="outside", cliponaxis=False)
left.plotly_chart(style(f3, 420, legend=False), use_container_width=True)

top_c = (df.groupby("Customer Name", as_index=False)[metric].sum()
           .nlargest(10, metric).sort_values(metric))
f4 = px.bar(top_c, x=metric, y="Customer Name", orientation="h",
            title=f"Top 10 Customers by {metric}", text_auto=".2s",
            color_discrete_sequence=[GREEN])
f4.update_traces(textposition="outside", cliponaxis=False)
right.plotly_chart(style(f4, 420, legend=False), use_container_width=True)

# ------------------------------------------------ discount vs margin
order = ["0%", "1-5%", "6-10%", "11-15%", "16-20%", "20%+"]
disc = (df.groupby("Discount Band", as_index=False)
          .agg(Sales=("Sales Amount", "sum"), Profit=("Profit", "sum"),
               Orders=("Order ID", "nunique")))
disc["Margin %"] = disc["Profit"] / disc["Sales"] * 100
disc["Discount Band"] = pd.Categorical(disc["Discount Band"], order, ordered=True)
disc = disc.sort_values("Discount Band")

left, right = st.columns((3, 2))
f5 = go.Figure()
f5.add_trace(go.Bar(x=disc["Discount Band"], y=disc["Sales"], name="Sales",
                    marker_color="#C9D9E8"))
f5.add_trace(go.Scatter(x=disc["Discount Band"], y=disc["Margin %"], name="Margin %",
                        mode="lines+markers", yaxis="y2",
                        line=dict(color=RED, width=3)))
f5.update_layout(title="Discount Band vs Profit Margin",
                 yaxis=dict(title="Sales ($)"),
                 yaxis2=dict(title="Margin %", overlaying="y", side="right",
                             showgrid=False))
left.plotly_chart(style(f5, 380), use_container_width=True)

pay = df.groupby("Payment Method", as_index=False)["Sales Amount"].sum()
f6 = px.pie(pay, names="Payment Method", values="Sales Amount", hole=0.55,
            title="Sales by Payment Method", color_discrete_sequence=PALETTE[1:])
f6.update_traces(textinfo="percent", textfont_size=11)
right.plotly_chart(style(f6, 380), use_container_width=True)

# ------------------------------------------------------ salespeople
sp = (df.groupby("Salesperson", as_index=False)
        .agg(Sales=("Sales Amount", "sum"), Profit=("Profit", "sum"),
             Orders=("Order ID", "nunique"))
        .sort_values("Sales", ascending=True))
f7 = px.bar(sp, x="Sales", y="Salesperson", orientation="h",
            title="Salesperson Leaderboard", text_auto=".2s",
            color="Profit", color_continuous_scale=["#C9D9E8", NAVY])
f7.update_traces(textposition="outside", cliponaxis=False)
f7.update_layout(coloraxis_colorbar=dict(title="Profit"))
st.plotly_chart(style(f7, max(360, 26 * len(sp) + 120), legend=False),
                use_container_width=True)

# ---------------------------------------------------------- details
st.subheader("Filtered records")
show_cols = ["Order ID", "Order Date", "Customer Name", "Region", "City",
             "Product Category", "Product Name", "Quantity", "Unit Price",
             "Discount", "Sales Amount", "Profit", "Payment Method", "Salesperson"]
st.dataframe(
    df[show_cols].sort_values("Order Date", ascending=False),
    use_container_width=True, hide_index=True, height=420,
    column_config={
        "Order Date": st.column_config.DateColumn(format="YYYY-MM-DD"),
        "Sales Amount": st.column_config.NumberColumn(format="$%.2f"),
        "Profit": st.column_config.NumberColumn(format="$%.2f"),
        "Unit Price": st.column_config.NumberColumn(format="$%.2f"),
        "Discount": st.column_config.NumberColumn(format="percent"),
    },
)
st.download_button("Download filtered data (CSV)",
                   df.to_csv(index=False).encode("utf-8"),
                   file_name="retail_sales_filtered.csv", mime="text/csv")

st.caption("Retail Sales Analytics · synthetic dataset · Streamlit + Plotly")
