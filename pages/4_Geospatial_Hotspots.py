# ============================================================
# GEOSPATIAL CLUSTER HOTSPOTS
# ============================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import (
    load_shop_df,
    load_master_df
)


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Geospatial Hotspots",
    page_icon="🗺️",
    layout="wide"
)


st.title("🗺️ Geospatial Cluster Hotspots")


# ============================================================
# LOAD DATA
# ============================================================

shop_df = load_shop_df()

master_df = load_master_df()


# ============================================================
# CHECK REQUIRED COLUMNS
# ============================================================

required_shop_cols = [
    "shopNo",
    "cluster"
]

required_geo_cols = [
    "shopNo",
    "latitude",
    "longitude"
]


missing_shop_cols = [
    col for col in required_shop_cols
    if col not in shop_df.columns
]


missing_geo_cols = [
    col for col in required_geo_cols
    if col not in master_df.columns
]


if missing_shop_cols:

    st.error(
        f"Missing columns in shop_df: {missing_shop_cols}"
    )

    st.stop()


if missing_geo_cols:

    st.error(
        f"Missing columns in master_df: {missing_geo_cols}"
    )

    st.stop()


# ============================================================
# GET GEO INFORMATION
# ============================================================

geo_df = master_df[
    [
        "shopNo",
        "latitude",
        "longitude"
    ]
].copy()


# ============================================================
# REMOVE DUPLICATE SHOPS
# ============================================================

geo_df = geo_df.drop_duplicates(
    subset=["shopNo"]
)


# ============================================================
# MERGE CLUSTER LABELS
# ============================================================

map_df = geo_df.merge(
    shop_df[
        [
            "shopNo",
            "cluster"
        ]
    ],
    on="shopNo",
    how="inner"
)


# ============================================================
# CLEAN COORDINATES
# ============================================================

map_df["latitude"] = pd.to_numeric(
    map_df["latitude"],
    errors="coerce"
)

map_df["longitude"] = pd.to_numeric(
    map_df["longitude"],
    errors="coerce"
)


map_df = map_df.dropna(
    subset=[
        "latitude",
        "longitude"
    ]
)


# ============================================================
# VALID COORDINATE RANGE
# ============================================================

map_df = map_df[
    (map_df["latitude"].between(-90, 90))
    &
    (map_df["longitude"].between(-180, 180))
]


# ============================================================
# CLUSTER FILTER
# ============================================================

clusters = sorted(
    map_df["cluster"]
    .dropna()
    .unique()
)


selected_clusters = st.multiselect(
    "🔵 Select Cluster(s)",
    clusters,
    default=clusters
)


map_df = map_df[
    map_df["cluster"].isin(
        selected_clusters
    )
]


# ============================================================
# CHECK DATA
# ============================================================

if map_df.empty:

    st.warning(
        "No shops available for the selected clusters."
    )

    st.stop()


# ============================================================
# KPI SECTION
# ============================================================

col1, col2, col3 = st.columns(3)


col1.metric(
    "🏪 Shops on Map",
    f"{map_df['shopNo'].nunique():,}"
)


col2.metric(
    "🔵 Clusters",
    f"{map_df['cluster'].nunique():,}"
)


col3.metric(
    "📍 Locations",
    f"{len(map_df):,}"
)


# ============================================================
# INTERACTIVE MAP
# ============================================================

st.subheader("📍 Shop Locations")


fig = px.scatter_map(
    map_df,
    lat="latitude",
    lon="longitude",
    color="cluster",
    hover_name="shopNo",
    hover_data={
        "latitude": ":.5f",
        "longitude": ":.5f",
        "cluster": True
    },
    zoom=6,
    height=650,
    title="Ration Shop Locations by Cluster"
)


fig.update_layout(
    map_style="open-street-map",
    margin={
        "r": 0,
        "t": 50,
        "l": 0,
        "b": 0
    }
)


st.plotly_chart(
    fig,
    use_container_width=True
)


# ============================================================
# CLUSTER DISTRIBUTION
# ============================================================

st.subheader(
    "📊 Cluster Distribution by Location"
)


cluster_counts = (
    map_df
    .groupby("cluster")["shopNo"]
    .nunique()
    .reset_index()
)


cluster_counts.columns = [
    "Cluster",
    "Number of Shops"
]


fig_cluster = px.bar(
    cluster_counts,
    x="Cluster",
    y="Number of Shops",
    text="Number of Shops",
    title="Number of Shops by Cluster"
)


fig_cluster.update_traces(
    textposition="outside"
)


st.plotly_chart(
    fig_cluster,
    use_container_width=True
)


# ============================================================
# MAP DATA TABLE
# ============================================================

st.subheader("🏪 Geospatial Shop Data")


st.dataframe(
    map_df,
    use_container_width=True,
    hide_index=True
)