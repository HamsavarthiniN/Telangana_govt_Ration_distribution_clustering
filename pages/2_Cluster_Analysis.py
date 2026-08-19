# ============================================================
# CLUSTER PROFILE REPORT
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import (
    load_shop_df,
    load_cluster_profile
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Cluster Analysis",
    page_icon="🔵",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🔵 Cluster Analysis")


# ============================================================
# LOAD DATA
# ============================================================

shop_df = load_shop_df()

cluster_profile = load_cluster_profile()


# ============================================================
# CHECK CLUSTER COLUMN
# ============================================================

if "cluster" not in shop_df.columns:

    st.error(
        "K-Means cluster labels were not found in shop_df."
    )

    st.stop()


# ============================================================
# CLUSTER SIZE
# ============================================================

cluster_counts = (
    shop_df["cluster"]
    .value_counts()
    .sort_index()
    .reset_index()
)

cluster_counts.columns = [
    "Cluster",
    "Number of Shops"
]


st.subheader("📊 Cluster Distribution")


fig = px.bar(
    cluster_counts,
    x="Cluster",
    y="Number of Shops",
    title="Number of Shops in Each Cluster"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CLUSTER PROFILE
# ============================================================

st.subheader("📋 Cluster Profile")

st.dataframe(
    cluster_profile,
    use_container_width=True
)


# ============================================================
# SELECT CLUSTER
# ============================================================

selected_cluster = st.selectbox(
    "Select Cluster",
    sorted(
        shop_df["cluster"]
        .dropna()
        .unique()
    )
)


cluster_data = shop_df[
    shop_df["cluster"] == selected_cluster
]


st.subheader(
    f"Cluster {selected_cluster} Characteristics"
)


# ============================================================
# CLUSTER METRICS
# ============================================================

col1, col2, col3 = st.columns(3)


if "avg_transactions" in cluster_data.columns:

    col1.metric(
        "Avg Transactions",
        f"{cluster_data['avg_transactions'].mean():,.0f}"
    )


if "avg_portability" in cluster_data.columns:

    col2.metric(
        "Avg Portability",
        f"{cluster_data['avg_portability'].mean():,.0f}"
    )


if "avg_amount" in cluster_data.columns:

    col3.metric(
        "Avg Amount",
        f"₹{cluster_data['avg_amount'].mean():,.0f}"
    )


# ============================================================
# FEATURE COMPARISON
# ============================================================

# Make sure the cluster column is available
# as a column rather than an index.

profile_plot = cluster_profile.copy()

if "cluster" not in profile_plot.columns:

    profile_plot = (
        profile_plot
        .reset_index()
    )


# Convert to long format

profile_long = profile_plot.melt(
    id_vars="cluster",
    var_name="Feature",
    value_name="Value"
)


# Plot

fig = px.bar(
    profile_long,
    x="Feature",
    y="Value",
    color="cluster",
    barmode="group",
    title="Cluster Feature Comparison"
)

st.plotly_chart(
    fig,
    use_container_width=True
)