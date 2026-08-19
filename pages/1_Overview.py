# ============================================================
# OVERVIEW DASHBOARD
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_shop_df


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Overview",
    page_icon="📊",
    layout="wide"
)


st.title("📊 Telangana Ration Shop Overview")


# ============================================================
# LOAD DATA
# ============================================================

shop_df = load_shop_df()


# ============================================================
# DATA CHECK
# ============================================================

if shop_df.empty:

    st.error("Shop dataset is empty.")

    st.stop()


# ============================================================
# SIDEBAR FILTERS
# ============================================================

st.sidebar.header("🔎 Filters")


# ------------------------------------------------------------
# DISTRICT FILTER
# ------------------------------------------------------------

if "distName" in shop_df.columns:

    districts = sorted(
        shop_df["distName"]
        .dropna()
        .astype(str)
        .unique()
    )

    selected_district = st.sidebar.selectbox(
        "District",
        ["All Districts"] + districts
    )

else:

    selected_district = "All Districts"


# ------------------------------------------------------------
# APPLY DISTRICT FILTER
# ------------------------------------------------------------

if selected_district == "All Districts":

    filtered_df = shop_df.copy()

else:

    filtered_df = shop_df[
        shop_df["distName"].astype(str)
        == selected_district
    ].copy()


# ============================================================
# KPI CARDS
# ============================================================

col1, col2, col3, col4 = st.columns(4)


# Total shops

total_shops = filtered_df["shopNo"].nunique()

col1.metric(
    "🏪 Total Shops",
    f"{total_shops:,}"
)


# Average transactions

if "avg_transactions" in filtered_df.columns:

    avg_transactions = filtered_df[
        "avg_transactions"
    ].mean()

    col2.metric(
        "🔄 Avg Transactions",
        f"{avg_transactions:,.0f}"
    )


# Average cards

if "avg_cards" in filtered_df.columns:

    avg_cards = filtered_df[
        "avg_cards"
    ].mean()

    col3.metric(
        "🪪 Avg Cards",
        f"{avg_cards:,.0f}"
    )


# Average portability

if "avg_portability" in filtered_df.columns:

    avg_portability = filtered_df[
        "avg_portability"
    ].mean()

    col4.metric(
        "🚚 Avg Portability",
        f"{avg_portability:,.0f}"
    )


# ============================================================
# CLUSTER DISTRIBUTION
# ============================================================

st.markdown("---")

if "cluster" in filtered_df.columns:

    st.subheader("🔵 Shop Distribution by Cluster")

    cluster_counts = (
        filtered_df
        .groupby("cluster")["shopNo"]
        .nunique()
        .reset_index()
    )

    cluster_counts.columns = [
        "Cluster",
        "Shops"
    ]

    fig = px.bar(
        cluster_counts,
        x="Cluster",
        y="Shops",
        text="Shops",
        title="Number of Shops in Each Cluster"
    )

    fig.update_traces(
        textposition="outside"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# DISTRICT SUMMARY
# ============================================================

st.markdown("---")

st.subheader("🗺️ District Summary")


if "distName" in shop_df.columns:

    district_summary = (
        filtered_df
        .groupby("distName")
        .agg(
            Shops=("shopNo", "nunique"),
            Avg_Transactions=(
                "avg_transactions",
                "mean"
            ),
            Avg_Cards=(
                "avg_cards",
                "mean"
            ),
            Avg_Portability=(
                "avg_portability",
                "mean"
            )
        )
        .reset_index()
    )

    district_summary = district_summary.round(2)

    st.dataframe(
        district_summary,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# SHOP DATA
# ============================================================

st.markdown("---")

st.subheader("🏪 Shop Data")


# ------------------------------------------------------------
# SEARCH SHOP
# ------------------------------------------------------------

search_shop = st.text_input(
    "🔎 Search Shop Number",
    placeholder="Enter shop number..."
)


display_df = filtered_df.copy()


if search_shop:

    display_df = display_df[
        display_df["shopNo"]
        .astype(str)
        .str.contains(
            search_shop,
            case=False,
            na=False
        )
    ]


# ------------------------------------------------------------
# DISPLAY COUNT
# ------------------------------------------------------------

st.write(
    f"Showing **{len(display_df):,} rows** "
    f"from **{filtered_df['shopNo'].nunique():,} shops**."
)


# ------------------------------------------------------------
# DATA TABLE
# ------------------------------------------------------------

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)