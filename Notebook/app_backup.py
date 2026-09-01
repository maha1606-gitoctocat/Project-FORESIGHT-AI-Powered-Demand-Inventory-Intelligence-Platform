import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="FORESIGHT - Retail Analytics",
    page_icon="📊",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("final_inventory_risk_output.csv")

df = load_data()

# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("📊 FORESIGHT – Retail Analytics Dashboard")

st.markdown(
    "### Forecast-driven inventory planning and risk management"
)

st.markdown("---")

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------

st.sidebar.header("🔎 Dashboard Filters")

# Store filter
store_options = sorted(df["store_id"].dropna().unique())

selected_stores = st.sidebar.multiselect(
    "Select Store",
    options=store_options,
    default=[]
)

# Category filter
category_options = sorted(df["category"].dropna().unique())

selected_categories = st.sidebar.multiselect(
    "Select Category",
    options=category_options,
    default=[]
)

# Brand filter
brand_options = sorted(df["brand"].dropna().unique())

selected_brands = st.sidebar.multiselect(
    "Select Brand",
    options=brand_options,
    default=[]
)

# Action filter
action_options = sorted(
    df["recommended_action"].dropna().unique()
)

selected_actions = st.sidebar.multiselect(
    "Recommended Action",
    options=action_options,
    default=[]
)

# --------------------------------------------------
# APPLY FILTERS
# --------------------------------------------------

filtered_df = df.copy()

if selected_stores:
    filtered_df = filtered_df[
        filtered_df["store_id"].isin(selected_stores)
    ]

if selected_categories:
    filtered_df = filtered_df[
        filtered_df["category"].isin(selected_categories)
    ]

if selected_brands:
    filtered_df = filtered_df[
        filtered_df["brand"].isin(selected_brands)
    ]

if selected_actions:
    filtered_df = filtered_df[
        filtered_df["recommended_action"].isin(selected_actions)
    ]

# --------------------------------------------------
# KPI CALCULATIONS
# --------------------------------------------------

total_records = len(filtered_df)

total_skus = filtered_df["sku_id"].nunique()

total_stores = filtered_df["store_id"].nunique()

total_value = filtered_df[
    "total_value_at_stake"
].sum()

stockout_value = filtered_df[
    "stockout_value_at_risk"
].sum()

overstock_value = filtered_df[
    "overstock_value_at_risk"
].sum()

reorder_count = (
    filtered_df["recommended_action"]
    .eq("Reorder Now")
    .sum()
)

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

st.subheader("📌 Inventory Risk Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Store-SKU Records",
        f"{total_records:,}"
    )

with col2:
    st.metric(
        "SKUs",
        f"{total_skus:,}"
    )

with col3:
    st.metric(
        "Stores",
        f"{total_stores:,}"
    )

with col4:
    st.metric(
        "Total Value at Stake",
        f"₹{total_value:,.0f}"
    )

# --------------------------------------------------
# SECOND KPI ROW
# --------------------------------------------------

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Stockout Value at Risk",
        f"₹{stockout_value:,.0f}"
    )

with col6:
    st.metric(
        "Overstock Value at Risk",
        f"₹{overstock_value:,.0f}"
    )

with col7:
    st.metric(
        "Reorder Now",
        f"{reorder_count:,}"
    )

st.markdown("---")

# --------------------------------------------------
# FILTER SUMMARY
# --------------------------------------------------

st.subheader("📋 Current Selection")

st.write(
    f"Showing **{len(filtered_df):,}** "
    f"store-SKU records."
)

# --------------------------------------------------
# RISK ANALYSIS
# --------------------------------------------------

st.markdown("---")

st.subheader("📊 Inventory Risk Analysis")

# --------------------------------------------------
# STOCKOUT VS OVERSTOCK RISK
# --------------------------------------------------

risk_summary = pd.DataFrame({
    "Risk Type": [
        "Stockout - High",
        "Stockout - Medium",
        "Overstock - High",
        "Overstock - Medium"
    ],
    "Count": [
        (filtered_df["forecast_stockout_risk"] == "HIGH").sum(),
        (filtered_df["forecast_stockout_risk"] == "MEDIUM").sum(),
        (filtered_df["forecast_overstock_risk"] == "HIGH").sum(),
        (filtered_df["forecast_overstock_risk"] == "MEDIUM").sum()
    ]
})

col1, col2 = st.columns(2)

with col1:

    st.markdown("#### 🔴 Stockout & Overstock Risk")

    st.bar_chart(
        risk_summary.set_index("Risk Type")
    )

# --------------------------------------------------
# RECOMMENDED ACTIONS
# --------------------------------------------------

action_summary = (
    filtered_df["recommended_action"]
    .value_counts()
    .reset_index()
)

action_summary.columns = [
    "Recommended Action",
    "Count"
]

with col2:

    st.markdown("#### 📋 Recommended Actions")

    st.bar_chart(
        action_summary.set_index(
            "Recommended Action"
        )
    )

# --------------------------------------------------
# CATEGORY RISK
# --------------------------------------------------

st.markdown("---")

st.markdown("#### 📦 Inventory Risk by Category")

category_summary = (
    filtered_df
    .groupby("category")["total_value_at_stake"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(category_summary)

# --------------------------------------------------
# TOP 10 SKUS BY VALUE AT STAKE
# --------------------------------------------------

st.markdown("---")

st.markdown("#### 💰 Top 10 SKUs by Value at Stake")

top_skus = (
    filtered_df[
        [
            "sku_id",
            "store_id",
            "category",
            "forecast_8_week_demand",
            "stock_on_hand",
            "total_value_at_stake",
            "recommended_action"
        ]
    ]
    .sort_values(
        "total_value_at_stake",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_skus,
    use_container_width=True
)

# --------------------------------------------------
# PRIORITY INVENTORY
# --------------------------------------------------

st.markdown("---")

st.subheader("🚨 Priority Inventory Actions")

st.write(
    "Items with the highest financial exposure and immediate inventory actions."
)

priority_inventory = (
    filtered_df[
        [
            "store_id",
            "sku_id",
            "category",
            "brand",
            "stock_on_hand",
            "forecast_8_week_demand",
            "stock_coverage_ratio",
            "forecast_stockout_risk",
            "forecast_overstock_risk",
            "recommended_action",
            "total_value_at_stake"
        ]
    ]
    .sort_values(
        "total_value_at_stake",
        ascending=False
    )
    .head(20)
)

st.dataframe(
    priority_inventory,
    use_container_width=True
)

# --------------------------------------------------
# FORECAST ANALYSIS
# --------------------------------------------------

st.markdown("---")

st.subheader("📈 8-Week Demand Forecast Analysis")

st.write(
    "Forecast-driven view of expected demand and current inventory coverage."
)

# --------------------------------------------------
# FORECAST SUMMARY
# --------------------------------------------------

forecast_summary = pd.DataFrame({
    "Metric": [
        "Average 8-Week Forecast",
        "Maximum 8-Week Forecast",
        "Minimum 8-Week Forecast"
    ],
    "Value": [
        filtered_df["forecast_8_week_demand"].mean(),
        filtered_df["forecast_8_week_demand"].max(),
        filtered_df["forecast_8_week_demand"].min()
    ]
})

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Average 8-Week Forecast",
        f"{filtered_df['forecast_8_week_demand'].mean():,.1f}"
    )

with col2:
    st.metric(
        "Highest 8-Week Forecast",
        f"{filtered_df['forecast_8_week_demand'].max():,.1f}"
    )

with col3:
    st.metric(
        "Lowest 8-Week Forecast",
        f"{filtered_df['forecast_8_week_demand'].min():,.1f}"
    )

# --------------------------------------------------
# TOP FORECAST DEMAND SKUS
# --------------------------------------------------

st.markdown("#### 🔥 Top 10 SKUs by Forecast Demand")

top_forecast = (
    filtered_df[
        [
            "sku_id",
            "store_id",
            "category",
            "stock_on_hand",
            "forecast_8_week_demand",
            "stock_coverage_ratio",
            "recommended_action"
        ]
    ]
    .sort_values(
        "forecast_8_week_demand",
        ascending=False
    )
    .head(10)
)

st.dataframe(
    top_forecast,
    use_container_width=True
)

# --------------------------------------------------
# STOCK VS FORECAST
# --------------------------------------------------

st.markdown("#### 📦 Current Stock vs 8-Week Forecast")

stock_forecast = (
    filtered_df[
        [
            "sku_id",
            "stock_on_hand",
            "forecast_8_week_demand"
        ]
    ]
    .sort_values(
        "forecast_8_week_demand",
        ascending=False
    )
    .head(15)
)

st.bar_chart(
    stock_forecast.set_index("sku_id")
)
