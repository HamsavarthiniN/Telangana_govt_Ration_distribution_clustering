import streamlit as st
import pandas as pd
import plotly.express as px

from data_loader import load_shop_df

st.set_page_config(
    page_title="Anomaly Detection",
    page_icon="⚠️",
    layout="wide"
)

st.title("⚠️ Anomaly Detection")

shop_df = load_shop_df()


# --------------------------------------------------
# CHECK DBSCAN LABEL
# --------------------------------------------------

if "dbscan_cluster" not in shop_df.columns:

    st.error(
        "DBSCAN labels were not found in shop_df."
    )

    st.info(
        "Make sure the DBSCAN labels are saved before "
        "saving shop_df.pkl."
    )

    st.stop()


# --------------------------------------------------
# LABEL COUNTS
# --------------------------------------------------

dbscan_counts = (
    shop_df["dbscan_cluster"]
    .value_counts()
    .sort_index()
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total Shops",
    shop_df["shopNo"].nunique()
)

col2.metric(
    "Normal Shops",
    (shop_df["dbscan_cluster"] != -1).sum()
)

col3.metric(
    "Anomalies",
    (shop_df["dbscan_cluster"] == -1).sum()
)


# --------------------------------------------------
# ANOMALY DATA
# --------------------------------------------------

anomalies = shop_df[
    shop_df["dbscan_cluster"] == -1
].copy()


st.subheader("Detected Anomalies")

if anomalies.empty:

    st.success("No DBSCAN anomalies detected.")

else:

    st.write(
        f"{len(anomalies)} shop records were identified "
        "as DBSCAN noise/outliers."
    )

    display_cols = [
        "shopNo",
        "distName",
        "avg_transactions",
        "avg_cards",
        "avg_portability",
        "avg_amount",
        "dbscan_cluster"
    ]

    display_cols = [
        col for col in display_cols
        if col in anomalies.columns
    ]

    st.dataframe(
        anomalies[display_cols],
        use_container_width=True
    )


# --------------------------------------------------
# NORMAL VS ANOMALY PROFILE
# --------------------------------------------------

st.subheader("Normal vs Anomaly Profile")

profile_features = [
    "avg_transactions",
    "transaction_cv",
    "avg_cards",
    "avg_portability",
    "afsc_transaction_share",
    "fsc_transaction_share",
    "aap_transaction_share",
    "avg_amount"
]

profile_features = [
    col for col in profile_features
    if col in shop_df.columns
]

profile = (
    shop_df
    .groupby("dbscan_cluster")[profile_features]
    .mean()
    .round(2)
)

st.dataframe(
    profile,
    use_container_width=True
)