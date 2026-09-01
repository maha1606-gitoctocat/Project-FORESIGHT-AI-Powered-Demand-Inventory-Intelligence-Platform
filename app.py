import streamlit as st
import pandas as pd


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="FORESIGHT | Inventory Intelligence",
    page_icon="📊",
    layout="wide"
)


# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():
    return pd.read_csv("final_inventory_risk_output.csv")


df = load_data()


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def format_crore(value):
    return f"₹{value / 10_000_000:,.2f} Cr"


# ==========================================================
# TITLE
# ==========================================================

st.title("📊 FORESIGHT")
st.markdown(
    "### Inventory Intelligence & Forecast-Driven Risk Management"
)

st.caption(
    "Using 8-week demand forecasts to identify inventory risks "
    "and recommend business actions."
)

st.markdown("---")


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("🔎 Dashboard Filters")

selected_stores = st.sidebar.multiselect(
    "Store",
    sorted(df["store_id"].dropna().unique())
)

selected_categories = st.sidebar.multiselect(
    "Category",
    sorted(df["category"].dropna().unique())
)

selected_brands = st.sidebar.multiselect(
    "Brand",
    sorted(df["brand"].dropna().unique())
)

selected_actions = st.sidebar.multiselect(
    "Recommended Action",
    sorted(df["recommended_action"].dropna().unique())
)


# ==========================================================
# FILTER DATA
# ==========================================================

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


# ==========================================================
# EMPTY FILTER CHECK
# ==========================================================

if filtered_df.empty:

    st.warning(
        "No records match the selected filters. "
        "Please change your selections."
    )

    st.stop()


# ==========================================================
# KPI CALCULATIONS
# ==========================================================

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


# ==========================================================
# KPI SECTION
# ==========================================================

st.subheader("📌 Executive Overview")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Store-SKU Records",
        f"{total_records:,}"
    )

with col2:
    st.metric(
        "Unique SKUs",
        f"{total_skus:,}"
    )

with col3:
    st.metric(
        "Stores",
        f"{total_stores:,}"
    )

with col4:
    st.metric(
        "Value at Stake",
        format_crore(total_value)
    )


col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "Stockout Exposure",
        format_crore(stockout_value)
    )

with col6:
    st.metric(
        "Overstock Exposure",
        format_crore(overstock_value)
    )

with col7:
    st.metric(
        "Reorder Now",
        f"{reorder_count:,}"
    )


st.markdown("---")


# ==========================================================
# TABS
# ==========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📊 Overview",
        "🚨 Risk Analysis",
        "📈 Forecast",
        "💰 Financial Impact",
        "📋 Priority Actions"
    ]
)


# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================

# ==========================================================
# TAB 1 — OVERVIEW
# ==========================================================

with tab1:

    st.subheader("📊 Inventory Overview")

    st.markdown(
        "High-level view of inventory actions, demand coverage "
        "and financial exposure."
    )

    # ------------------------------------------------------
    # RECOMMENDED ACTIONS
    # ------------------------------------------------------

    st.markdown("### 📋 Recommended Actions")

    action_summary = (
        filtered_df["recommended_action"]
        .value_counts()
        .reindex(
            [
                "Reorder Now",
                "Watch / Replenish Soon",
                "Healthy",
                "Watch / Reduce Orders",
                "Clear / Markdown"
            ],
            fill_value=0
        )
    )

    st.bar_chart(
        action_summary,
        width="stretch"
    )

    # ------------------------------------------------------
    # VALUE AT STAKE BY CATEGORY
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown("### 💰 Value at Stake by Category")

    category_value = (
        filtered_df
        .groupby("category")[
            "total_value_at_stake"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    # Convert ₹ to ₹ Crores
    category_value_crore = (
        category_value / 10_000_000
    )

    category_value_crore.name = (
        "Value at Stake (₹ Cr)"
    )

    st.bar_chart(
        category_value_crore,
        width="stretch"
    )

    # ------------------------------------------------------
    # INVENTORY HEALTH SNAPSHOT
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown("### 📦 Inventory Health Snapshot")

    healthy_count = (
        filtered_df["recommended_action"]
        .eq("Healthy")
        .sum()
    )

    reorder_count = (
        filtered_df["recommended_action"]
        .eq("Reorder Now")
        .sum()
    )

    markdown_count = (
        filtered_df["recommended_action"]
        .eq("Clear / Markdown")
        .sum()
    )

    reduce_order_count = (
        filtered_df["recommended_action"]
        .eq("Watch / Reduce Orders")
        .sum()
    )

    replenish_count = (
        filtered_df["recommended_action"]
        .eq("Watch / Replenish Soon")
        .sum()
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "Healthy",
            f"{healthy_count:,}"
        )

    with col2:
        st.metric(
            "Reorder Now",
            f"{reorder_count:,}"
        )

    with col3:
        st.metric(
            "Clear / Markdown",
            f"{markdown_count:,}"
        )

    with col4:
        st.metric(
            "Reduce Orders",
            f"{reduce_order_count:,}"
        )

    with col5:
        st.metric(
            "Replenish Soon",
            f"{replenish_count:,}"
        )

    # ------------------------------------------------------
    # TOP 10 SKUs BY VALUE AT STAKE
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 🔝 Top 10 SKUs by Value at Stake"
    )

    top_skus = (
        filtered_df[
            [
                "sku_id",
                "store_id",
                "category",
                "stock_on_hand",
                "forecast_8_week_demand",
                "total_value_at_stake",
                "recommended_action"
            ]
        ]
        .sort_values(
            "total_value_at_stake",
            ascending=False
        )
        .head(10)
        .copy()
    )

    # Display financial value in ₹ Crores
    top_skus["total_value_at_stake"] = (
        top_skus["total_value_at_stake"] / 10_000_000
    )

    top_skus = top_skus.rename(
        columns={
            "sku_id": "SKU",
            "store_id": "Store",
            "category": "Category",
            "stock_on_hand": "Stock on Hand",
            "forecast_8_week_demand": "8-Week Forecast",
            "total_value_at_stake": "Value at Stake (₹ Cr)",
            "recommended_action": "Recommended Action"
        }
    )

    st.dataframe(
        top_skus,
        width="stretch",
        hide_index=True
    )

# ==========================================================
# TAB 2 — RISK ANALYSIS
# ==========================================================

# ==========================================================
# TAB 2 — RISK ANALYSIS
# ==========================================================

with tab2:

    st.subheader("🚨 Inventory Risk Analysis")

    st.markdown(
        "Identify forecast-driven stockout and overstock risks "
        "and understand where financial exposure is concentrated."
    )

    # ------------------------------------------------------
    # STOCKOUT AND OVERSTOCK RISK
    # ------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🔴 Stockout Risk")

        stockout_summary = (
            filtered_df[
                "forecast_stockout_risk"
            ]
            .value_counts()
            .reindex(
                ["HIGH", "MEDIUM", "LOW"],
                fill_value=0
            )
        )

        st.bar_chart(
            stockout_summary,
            width="stretch"
        )

    with col2:

        st.markdown("### 🟠 Overstock Risk")

        overstock_summary = (
            filtered_df[
                "forecast_overstock_risk"
            ]
            .value_counts()
            .reindex(
                ["HIGH", "MEDIUM", "LOW"],
                fill_value=0
            )
        )

        st.bar_chart(
            overstock_summary,
            width="stretch"
        )

    # ------------------------------------------------------
    # RISK COUNTS
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown("### 📌 Risk Summary")

    stockout_high = (
        filtered_df["forecast_stockout_risk"]
        .eq("HIGH")
        .sum()
    )

    stockout_medium = (
        filtered_df["forecast_stockout_risk"]
        .eq("MEDIUM")
        .sum()
    )

    overstock_high = (
        filtered_df["forecast_overstock_risk"]
        .eq("HIGH")
        .sum()
    )

    overstock_medium = (
        filtered_df["forecast_overstock_risk"]
        .eq("MEDIUM")
        .sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "High Stockout Risk",
            f"{stockout_high:,}"
        )

    with col2:
        st.metric(
            "Medium Stockout Risk",
            f"{stockout_medium:,}"
        )

    with col3:
        st.metric(
            "High Overstock Risk",
            f"{overstock_high:,}"
        )

    with col4:
        st.metric(
            "Medium Overstock Risk",
            f"{overstock_medium:,}"
        )

    # ------------------------------------------------------
    # FINANCIAL RISK BY CATEGORY
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 💰 Financial Risk by Category"
    )

    category_risk = (
        filtered_df
        .groupby("category")[
            "total_value_at_stake"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    # Convert ₹ to ₹ Crores
    category_risk_crore = (
        category_risk / 10_000_000
    )

    category_risk_crore.name = (
        "Risk Exposure (₹ Cr)"
    )

    st.bar_chart(
        category_risk_crore,
        width="stretch"
    )

    # ------------------------------------------------------
    # TOP RISK RECORDS
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 🔝 Highest-Value Risk Records"
    )

    top_risk = (
        filtered_df[
            [
                "store_id",
                "sku_id",
                "category",
                "stock_on_hand",
                "forecast_8_week_demand",
                "forecast_stockout_risk",
                "forecast_overstock_risk",
                "total_value_at_stake",
                "recommended_action"
            ]
        ]
        .sort_values(
            "total_value_at_stake",
            ascending=False
        )
        .head(15)
        .copy()
    )

    top_risk["total_value_at_stake"] = (
        top_risk["total_value_at_stake"] / 10_000_000
    )

    top_risk = top_risk.rename(
        columns={
            "store_id": "Store",
            "sku_id": "SKU",
            "category": "Category",
            "stock_on_hand": "Stock on Hand",
            "forecast_8_week_demand": "8-Week Forecast",
            "forecast_stockout_risk": "Stockout Risk",
            "forecast_overstock_risk": "Overstock Risk",
            "total_value_at_stake": "Value at Stake (₹ Cr)",
            "recommended_action": "Recommended Action"
        }
    )

    st.dataframe(
        top_risk,
        width="stretch",
        hide_index=True
    )

# ==========================================================
# TAB 3 — FORECAST
# ==========================================================

with tab3:

    st.subheader("📈 Demand Forecast Analysis")

    st.markdown(
        "Analyze 8-week demand forecasts and compare expected demand "
        "with current inventory levels."
    )

    # ------------------------------------------------------
    # FORECAST KPIs
    # ------------------------------------------------------

    total_forecast_demand = (
        filtered_df["forecast_8_week_demand"]
        .sum()
    )

    avg_forecast_demand = (
        filtered_df["forecast_8_week_demand"]
        .mean()
    )

    max_forecast_demand = (
        filtered_df["forecast_8_week_demand"]
        .max()
    )

    total_stock = (
        filtered_df["stock_on_hand"]
        .sum()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "8-Week Forecast Demand",
            f"{total_forecast_demand:,.0f}"
        )

    with col2:
        st.metric(
            "Average Forecast / SKU",
            f"{avg_forecast_demand:,.1f}"
        )

    with col3:
        st.metric(
            "Highest SKU Forecast",
            f"{max_forecast_demand:,.1f}"
        )

    with col4:
        st.metric(
            "Current Stock on Hand",
            f"{total_stock:,.0f}"
        )

    # ------------------------------------------------------
    # TOP SKUs BY FORECAST DEMAND
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 🔝 Top 10 SKUs by Forecast Demand"
    )

    top_forecast = (
        filtered_df[
            [
                "sku_id",
                "store_id",
                "category",
                "brand",
                "stock_on_hand",
                "forecast_8_week_demand",
                "forecast_stockout_risk",
                "recommended_action"
            ]
        ]
        .sort_values(
            "forecast_8_week_demand",
            ascending=False
        )
        .head(10)
        .copy()
    )

    top_forecast = top_forecast.rename(
        columns={
            "sku_id": "SKU",
            "store_id": "Store",
            "category": "Category",
            "brand": "Brand",
            "stock_on_hand": "Stock on Hand",
            "forecast_8_week_demand": "8-Week Forecast",
            "forecast_stockout_risk": "Stockout Risk",
            "recommended_action": "Recommended Action"
        }
    )

    st.dataframe(
        top_forecast,
        width="stretch",
        hide_index=True
    )

    # ------------------------------------------------------
    # FORECAST VS CURRENT STOCK
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 📊 Current Stock vs 8-Week Forecast"
    )

    forecast_comparison = (
        filtered_df
        .groupby("category")[
            [
                "stock_on_hand",
                "forecast_8_week_demand"
            ]
        ]
        .sum()
        .sort_values(
            "forecast_8_week_demand",
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(
        forecast_comparison,
        width="stretch"
    )

    # ------------------------------------------------------
    # FORECAST DEMAND BY CATEGORY
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 📦 Forecast Demand by Category"
    )

    category_forecast = (
        filtered_df
        .groupby("category")[
            "forecast_8_week_demand"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(10)
    )

    st.bar_chart(
        category_forecast,
        width="stretch"
    )

    # ------------------------------------------------------
    # HIGH DEMAND + LOW STOCK
    # ------------------------------------------------------

     # ------------------------------------------------------
    # HIGH DEMAND + LOW STOCK
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### ⚠️ High Demand & Low Stock"
    )

    high_demand_low_stock = (
        filtered_df[
            filtered_df["forecast_8_week_demand"]
            > filtered_df["stock_on_hand"]
        ][
            [
                "store_id",
                "sku_id",
                "category",
                "stock_on_hand",
                "forecast_8_week_demand",
                "forecast_stockout_risk",
                "recommended_action"
            ]
        ]
        .sort_values(
            "forecast_8_week_demand",
            ascending=False
        )
        .head(15)
        .copy()
    )

    high_demand_low_stock = high_demand_low_stock.rename(
        columns={
            "store_id": "Store",
            "sku_id": "SKU",
            "category": "Category",
            "stock_on_hand": "Stock on Hand",
            "forecast_8_week_demand": "8-Week Forecast",
            "forecast_stockout_risk": "Stockout Risk",
            "recommended_action": "Recommended Action"
        }
    )

    st.dataframe(
        high_demand_low_stock,
        width="stretch",
        hide_index=True
    )


# ==========================================================
# TAB 4 — FINANCIAL IMPACT
# ==========================================================

with tab4:
	

    st.subheader("💰 Financial Impact Analysis")

    st.markdown(
        "Measure the financial exposure created by forecast-driven "
        "stockout and overstock risks."
    )


    # ------------------------------------------------------
    # FINANCIAL KPIs
    # ------------------------------------------------------

    total_value_stake = (
        filtered_df["total_value_at_stake"].sum()
    )

    total_stockout_value = (
        filtered_df["stockout_value_at_risk"].sum()
    )

    total_overstock_value = (
        filtered_df["overstock_value_at_risk"].sum()
    )

    avg_value_stake = (
        filtered_df["total_value_at_stake"].mean()
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Value at Stake",
            f"₹{total_value_stake / 10000000:.2f} Cr"
        )

    with col2:
        st.metric(
            "Stockout Exposure",
            f"₹{total_stockout_value / 10000000:.2f} Cr"
        )

    with col3:
        st.metric(
            "Overstock Exposure",
            f"₹{total_overstock_value / 10000000:.2f} Cr"
        )

    with col4:
        st.metric(
            "Average Value / Record",
            f"₹{avg_value_stake:,.0f}"
        )

    st.markdown("---")

    # ------------------------------------------------------
    # STOCKOUT VS OVERSTOCK
    # ------------------------------------------------------

    st.markdown(
        "#### 📊 Stockout vs Overstock Financial Exposure (₹ Cr)"
    )

    exposure_data = pd.Series(
        {
            "Stockout Exposure": total_stockout_value / 10000000,
            "Overstock Exposure": total_overstock_value / 10000000
        }
    )

    st.bar_chart(
        exposure_data,
        width="stretch"
    )

    st.markdown("---")

    # ------------------------------------------------------
    # VALUE AT STAKE BY CATEGORY
    # ------------------------------------------------------

    st.markdown(
        "#### 📦 Value at Stake by Category (₹ Cr)"
    )

    category_value = (
        filtered_df
        .groupby("category")["total_value_at_stake"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        / 10000000
    )

    st.bar_chart(
        category_value,
        width="stretch"
    )

    st.markdown("---")

    # ------------------------------------------------------
    # VALUE AT STAKE BY STORE
    # ------------------------------------------------------

    st.markdown(
        "#### 🏪 Value at Stake by Store (₹ Cr)"
    )

    store_value = (
        filtered_df
        .groupby("store_id")["total_value_at_stake"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
        / 10000000
    )

    st.bar_chart(
        store_value,
        width="stretch"
    )
    # ------------------------------------------------------
    # TOP 10 FINANCIAL RISKS
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 🔝 Top 10 Inventory Risks by Financial Exposure"
    )

    top_financial_risks = (
        filtered_df[
            [
                "store_id",
                "sku_id",
                "category",
                "brand",
                "stock_on_hand",
                "forecast_8_week_demand",
                "forecast_stockout_risk",
                "forecast_overstock_risk",
                "recommended_action",
                "stockout_value_at_risk",
                "overstock_value_at_risk",
                "total_value_at_stake"
            ]
        ]
        .sort_values(
            "total_value_at_stake",
            ascending=False
        )
        .head(10)
        .copy()
    )

    top_financial_risks = top_financial_risks.rename(
        columns={
            "store_id": "Store",
            "sku_id": "SKU",
            "category": "Category",
            "brand": "Brand",
            "stock_on_hand": "Stock on Hand",
            "forecast_8_week_demand": "8-Week Forecast",
            "forecast_stockout_risk": "Stockout Risk",
            "forecast_overstock_risk": "Overstock Risk",
            "recommended_action": "Recommended Action",
            "stockout_value_at_risk": "Stockout Value at Risk",
            "overstock_value_at_risk": "Overstock Value at Risk",
            "total_value_at_stake": "Total Value at Stake"
        }
    )

    st.dataframe(
        top_financial_risks,
        width="stretch",
        hide_index=True
    )

    # ------------------------------------------------------
    # FINANCIAL INTERPRETATION
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown("### 💡 Financial Risk Interpretation")

    if total_stockout_value > total_overstock_value:

        st.warning(
            "Stockout exposure is currently higher than overstock "
            "exposure. Replenishment and availability should receive "
            "priority attention."
        )

    elif total_overstock_value > total_stockout_value:

        st.warning(
            "Overstock exposure is currently higher than stockout "
            "exposure. Inventory reduction and demand-aligned ordering "
            "should receive priority attention."
        )

    else:

        st.info(
            "Stockout and overstock exposures are currently balanced."
        )

# ==========================================================
# TAB 5 — PRIORITY ACTIONS
# ==========================================================

with tab5:

    st.subheader("📋 Priority Inventory Actions")

    st.markdown(
        "Prioritize inventory decisions based on forecast risk, "
        "current stock levels and financial exposure."
    )

    # ------------------------------------------------------
    # ACTION COUNTS
    # ------------------------------------------------------

    action_counts = (
        filtered_df["recommended_action"]
        .value_counts()
        .reindex(
            [
                "Reorder Now",
                "Watch / Replenish Soon",
                "Watch / Reduce Orders",
                "Clear / Markdown",
                "Healthy"
            ],
            fill_value=0
        )
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            "🔴 Reorder Now",
            f"{action_counts['Reorder Now']:,}"
        )

    with col2:
        st.metric(
            "🟠 Replenish Soon",
            f"{action_counts['Watch / Replenish Soon']:,}"
        )

    with col3:
        st.metric(
            "🟡 Reduce Orders",
            f"{action_counts['Watch / Reduce Orders']:,}"
        )

    with col4:
        st.metric(
            "🔵 Clear / Markdown",
            f"{action_counts['Clear / Markdown']:,}"
        )

    with col5:
        st.metric(
            "🟢 Healthy",
            f"{action_counts['Healthy']:,}"
        )

    # ------------------------------------------------------
    # ACTION DISTRIBUTION
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 📊 Recommended Action Distribution"
    )

    st.bar_chart(
        action_counts,
        width="stretch"
    )

    # ------------------------------------------------------
    # PRIORITY RECORDS
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 🔝 Highest-Priority Inventory Records"
    )

    priority_df = (
        filtered_df[
            [
                "store_id",
                "sku_id",
                "category",
                "brand",
                "stock_on_hand",
                "reorder_point",
                "safety_stock",
                "forecast_8_week_demand",
                "stock_coverage_ratio",
                "forecast_stockout_risk",
                "forecast_overstock_risk",
                "recommended_action",
                "total_value_at_stake"
            ]
        ]
        .copy()
    )

    # Give urgent actions higher priority
    action_priority = {
        "Reorder Now": 1,
        "Watch / Replenish Soon": 2,
        "Watch / Reduce Orders": 3,
        "Clear / Markdown": 4,
        "Healthy": 5
    }

    priority_df["action_priority"] = (
        priority_df["recommended_action"]
        .map(action_priority)
        .fillna(99)
    )

    priority_df = (
        priority_df
        .sort_values(
            [
                "action_priority",
                "total_value_at_stake"
            ],
            ascending=[
                True,
                False
            ]
        )
        .head(20)
        .copy()
    )

    priority_df = priority_df.rename(
        columns={
            "store_id": "Store",
            "sku_id": "SKU",
            "category": "Category",
            "brand": "Brand",
            "stock_on_hand": "Stock on Hand",
            "reorder_point": "Reorder Point",
            "safety_stock": "Safety Stock",
            "forecast_8_week_demand": "8-Week Forecast",
            "stock_coverage_ratio": "Stock Coverage",
            "forecast_stockout_risk": "Stockout Risk",
            "forecast_overstock_risk": "Overstock Risk",
            "recommended_action": "Recommended Action",
            "total_value_at_stake": "Value at Stake"
        }
    )

    priority_df = priority_df.drop(
        columns=["action_priority"]
    )

    st.dataframe(
        priority_df,
        width="stretch",
        hide_index=True
    )

    # ------------------------------------------------------
    # REORDER NOW
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 🔴 Reorder Now"
    )

    reorder_df = (
        filtered_df[
            filtered_df["recommended_action"]
            == "Reorder Now"
        ][
            [
                "store_id",
                "sku_id",
                "category",
                "stock_on_hand",
                "reorder_point",
                "forecast_8_week_demand",
                "stock_coverage_ratio",
                "stockout_value_at_risk",
                "total_value_at_stake"
            ]
        ]
        .sort_values(
            "total_value_at_stake",
            ascending=False
        )
        .head(15)
        .copy()
    )

    reorder_df = reorder_df.rename(
        columns={
            "store_id": "Store",
            "sku_id": "SKU",
            "category": "Category",
            "stock_on_hand": "Stock on Hand",
            "reorder_point": "Reorder Point",
            "forecast_8_week_demand": "8-Week Forecast",
            "stock_coverage_ratio": "Stock Coverage",
            "stockout_value_at_risk": "Stockout Value at Risk",
            "total_value_at_stake": "Total Value at Stake"
        }
    )

    st.dataframe(
        reorder_df,
        width="stretch",
        hide_index=True
    )

    # ------------------------------------------------------
    # OVERSTOCK ACTIONS
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 🔵 Overstock Reduction Opportunities"
    )

    overstock_df = (
        filtered_df[
            filtered_df["recommended_action"]
            == "Clear / Markdown"
        ][
            [
                "store_id",
                "sku_id",
                "category",
                "brand",
                "stock_on_hand",
                "forecast_8_week_demand",
                "stock_coverage_ratio",
                "overstock_value_at_risk",
                "total_value_at_stake"
            ]
        ]
        .sort_values(
            "total_value_at_stake",
            ascending=False
        )
        .head(15)
        .copy()
    )

    overstock_df = overstock_df.rename(
        columns={
            "store_id": "Store",
            "sku_id": "SKU",
            "category": "Category",
            "brand": "Brand",
            "stock_on_hand": "Stock on Hand",
            "forecast_8_week_demand": "8-Week Forecast",
            "stock_coverage_ratio": "Stock Coverage",
            "overstock_value_at_risk": "Overstock Value at Risk",
            "total_value_at_stake": "Total Value at Stake"
        }
    )

    st.dataframe(
        overstock_df,
        width="stretch",
        hide_index=True
    )

    # ------------------------------------------------------
    # MANAGEMENT MESSAGE
    # ------------------------------------------------------

    st.markdown("---")

    st.markdown(
        "### 💡 Management Priority"
    )

    if action_counts["Reorder Now"] > action_counts["Clear / Markdown"]:

        st.info(
            "Replenishment is the dominant immediate action. "
            "Management should prioritize products with high forecast "
            "demand and insufficient inventory coverage."
        )

    elif action_counts["Clear / Markdown"] > action_counts["Reorder Now"]:

        st.info(
            "Inventory reduction is the dominant immediate action. "
            "Management should focus on excess stock, markdowns and "
            "reducing future purchase quantities."
        )

    else:

        st.info(
            "Replenishment and inventory reduction actions are relatively "
            "balanced. Decisions should be prioritized using financial "
            "exposure and forecast demand."
        )

# ==========================================================
# DOWNLOAD FILTERED DATA
# ==========================================================

st.markdown("---")

st.subheader("⬇️ Export Dashboard Data")

st.markdown(
    "Download the currently filtered inventory risk records "
    "for further analysis or reporting."
)

download_data = filtered_df.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="⬇️ Download Filtered Inventory Data",
    data=download_data,
    file_name="FORESIGHT_filtered_inventory_risk.csv",
    mime="text/csv",
    width="stretch"
)