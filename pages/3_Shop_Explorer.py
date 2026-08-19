#Search Tool to input a shopNo and see its performance compared to its cluster average.
import streamlit as st
import pandas as pd

from data_loader import load_shop_df

st.set_page_config(
    page_title="Shop Explorer",
    page_icon="🔎",
    layout="wide"
)

st.title("🔎 Shop Explorer")

shop_df = load_shop_df()

# --------------------------------------------------
# SHOP SEARCH
# --------------------------------------------------

shop_numbers = (
    shop_df["shopNo"]
    .dropna()
    .unique()
)

selected_shop = st.selectbox(
    "Search Shop Number",
    sorted(shop_numbers, key=str)
)

shop = shop_df[
    shop_df["shopNo"] == selected_shop
]

if shop.empty:

    st.warning("Shop not found.")

    st.stop()


shop = shop.iloc[0]


# --------------------------------------------------
# SHOP INFORMATION
# --------------------------------------------------

st.subheader(f"Shop: {selected_shop}")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "District",
    shop.get("distName", "Unknown")
)

col2.metric(
    "Cluster",
    shop.get("cluster", "N/A")
)

col3.metric(
    "Avg Transactions",
    f"{shop.get('avg_transactions', 0):,.0f}"
)

col4.metric(
    "Avg Portability",
    f"{shop.get('avg_portability', 0):,.0f}"
)


# --------------------------------------------------
# CLUSTER COMPARISON
# --------------------------------------------------

if "cluster" in shop_df.columns:

    cluster_id = shop["cluster"]

    cluster_data = shop_df[
        shop_df["cluster"] == cluster_id
    ]

    st.subheader(
        f"Shop Performance vs Cluster {cluster_id} Average"
    )

    comparison_features = [
        "avg_transactions",
        "transaction_cv",
        "avg_cards",
        "avg_portability",
        "afsc_transaction_share",
        "fsc_transaction_share",
        "aap_transaction_share",
        "avg_amount"
    ]

    comparison_features = [
        col for col in comparison_features
        if col in shop_df.columns
    ]

    comparison = []

    for feature in comparison_features:

        shop_value = shop[feature]

        cluster_value = cluster_data[feature].mean()

        if cluster_value != 0:

            difference_pct = (
                (shop_value - cluster_value)
                / abs(cluster_value)
            ) * 100

        else:
            difference_pct = None

        comparison.append({
            "Feature": feature,
            "Shop Value": shop_value,
            "Cluster Average": cluster_value,
            "Difference %": difference_pct
        })

    comparison_df = pd.DataFrame(comparison)

    st.dataframe(
        comparison_df.round(2),
        use_container_width=True
    )


# --------------------------------------------------
# INTERPRETATION
# --------------------------------------------------

st.subheader("Performance Interpretation")

if "avg_transactions" in shop_df.columns:

    cluster_avg = cluster_data[
        "avg_transactions"
    ].mean()

    if shop["avg_transactions"] > cluster_avg * 1.2:

        st.success(
            "This shop has significantly higher transaction "
            "volume than its cluster average."
        )

    elif shop["avg_transactions"] < cluster_avg * 0.8:

        st.warning(
            "This shop has significantly lower transaction "
            "volume than its cluster average."
        )

    else:

        st.info(
            "This shop's transaction volume is broadly "
            "consistent with its cluster."
        )