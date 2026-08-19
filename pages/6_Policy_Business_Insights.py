import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from data_loader import load_shop_df, load_master_df


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Policy & Business Insights",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Policy & Business Insights")

st.markdown("""
This page translates the clustering results into three major
business use cases:

- 🏛️ Policy Impact Analysis
- ⚠️ Fraud Prevention
- 🚚 Logistics Optimization
""")


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    shop_df = load_shop_df()
    master_df = load_master_df()

    return shop_df, master_df


shop_df, master_df = load_data()


# ============================================================
# CREATE TABS
# ============================================================

tab1, tab2, tab3 = st.tabs([
    "🏛️ Policy Impact",
    "⚠️ Fraud Prevention",
    "🚚 Logistics Optimization"
])


# ============================================================
# TAB 1 — POLICY IMPACT
# ============================================================

with tab1:

    st.header("🏛️ Policy Impact Analysis")

    st.markdown("""
    **Objective:** Identify how portability activity changed after
    implementation of the One Nation One Ration Card (ONORC) policy.
    """)

    # --------------------------------------------------------
    # CHECK REQUIRED COLUMNS
    # --------------------------------------------------------

    required_cols = [
        "year",
        "noOfTrans",
        "otherShopTransCnt"
    ]

    missing = [
        col for col in required_cols
        if col not in master_df.columns
    ]

    if missing:

        st.warning(
            f"Required columns are missing: {missing}"
        )

    else:

        # ----------------------------------------------------
        # YEARLY AGGREGATION
        # ----------------------------------------------------

        yearly = (
            master_df
            .groupby("year")
            .agg(
                total_transactions=("noOfTrans", "sum"),
                total_portability=("otherShopTransCnt", "sum")
            )
            .reset_index()
        )

        yearly["portability_ratio"] = np.where(
            yearly["total_transactions"] > 0,
            yearly["total_portability"] /
            yearly["total_transactions"],
            np.nan
        )

        # ----------------------------------------------------
        # DISPLAY YEARLY DATA
        # ----------------------------------------------------

        st.subheader("Year-wise Portability Trend")

        fig = px.line(
            yearly,
            x="year",
            y="portability_ratio",
            markers=True,
            title="Portability Ratio Over Time"
        )

        fig.update_yaxes(
            tickformat=".1%"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # TRANSACTION + PORTABILITY
        # ----------------------------------------------------

        st.subheader("Transactions vs Portability")

        trend = yearly.melt(
            id_vars="year",
            value_vars=[
                "total_transactions",
                "total_portability"
            ],
            var_name="Metric",
            value_name="Value"
        )

        fig2 = px.line(
            trend,
            x="year",
            y="Value",
            color="Metric",
            markers=True,
            title="Transaction and Portability Trends"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        # ----------------------------------------------------
        # YEARLY TABLE
        # ----------------------------------------------------

        st.subheader("Policy Impact Summary")

        st.dataframe(
            yearly.round(3),
            use_container_width=True
        )

        st.info("""
        **Interpretation:** An increase in portability ratio over
        time indicates that more beneficiaries are transacting at
        shops other than their original/registered shop, suggesting
        increased portability activity after policy implementation.
        """)


# ============================================================
# TAB 2 — FRAUD PREVENTION
# ============================================================

with tab2:

    st.header("⚠️ Fraud Prevention")

    st.markdown("""
    **Objective:** Flag shops whose transaction-to-card ratio
    deviates significantly from the average behavior of their
    K-Means peer cluster.
    """)

    # --------------------------------------------------------
    # CHECK REQUIRED COLUMNS
    # --------------------------------------------------------

    required = [
        "shopNo",
        "cluster",
        "total_transactions",
        "total_cards"
    ]

    missing = [
        col for col in required
        if col not in shop_df.columns
    ]

    if missing:

        st.warning(
            f"Required columns are missing from shop_df: {missing}"
        )

    else:

        # ----------------------------------------------------
        # CALCULATE UTILIZATION RATIO
        # ----------------------------------------------------

        fraud_df = shop_df.copy()

        fraud_df["utilization_ratio"] = (
            fraud_df["total_transactions"] /
            fraud_df["total_cards"].replace(
                0,
                np.nan
            )
        )

        # ----------------------------------------------------
        # CLUSTER AVERAGE
        # ----------------------------------------------------

        cluster_avg = (
            fraud_df
            .groupby("cluster")["utilization_ratio"]
            .transform("mean")
        )

        fraud_df["cluster_avg_utilization"] = cluster_avg

        # ----------------------------------------------------
        # DEVIATION %
        # ----------------------------------------------------

        fraud_df["utilization_deviation_pct"] = np.where(
            fraud_df["cluster_avg_utilization"] != 0,

            (
                (
                    fraud_df["utilization_ratio"]
                    -
                    fraud_df["cluster_avg_utilization"]
                )
                /
                abs(
                    fraud_df["cluster_avg_utilization"]
                )
            ) * 100,

            np.nan
        )

        # ----------------------------------------------------
        # FLAG SHOPS
        # ----------------------------------------------------

        threshold = st.slider(
            "Deviation threshold (%)",
            min_value=10,
            max_value=100,
            value=30,
            step=5
        )

        fraud_df["fraud_flag"] = np.where(
            abs(
                fraud_df["utilization_deviation_pct"]
            ) >= threshold,
            "Review Required",
            "Normal"
        )

        # ----------------------------------------------------
        # KPI
        # ----------------------------------------------------

        flagged = fraud_df[
            fraud_df["fraud_flag"] == "Review Required"
        ]

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Shops",
            len(fraud_df)
        )

        col2.metric(
            "Flagged Shops",
            len(flagged)
        )

        col3.metric(
            "Flagged %",
            f"{len(flagged) / len(fraud_df) * 100:.2f}%"
        )

        # ----------------------------------------------------
        # DEVIATION CHART
        # ----------------------------------------------------

        st.subheader(
            "Transaction/Card Ratio Deviation"
        )

        plot_df = fraud_df.copy()

        plot_df["Deviation"] = (
            plot_df["utilization_deviation_pct"]
        )

        fig = px.histogram(
            plot_df,
            x="Deviation",
            nbins=40,
            title="Distribution of Utilization Deviation"
        )

        fig.add_vline(
            x=threshold,
            line_dash="dash"
        )

        fig.add_vline(
            x=-threshold,
            line_dash="dash"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # FLAGGED SHOP TABLE
        # ----------------------------------------------------

        st.subheader(
            "🚨 Shops Requiring Review"
        )

        display_cols = [
            "shopNo",
            "cluster",
            "utilization_ratio",
            "cluster_avg_utilization",
            "utilization_deviation_pct",
            "fraud_flag"
        ]

        display_cols = [
            col for col in display_cols
            if col in fraud_df.columns
        ]

        flagged_display = (
            flagged[
                display_cols
            ]
            .sort_values(
                "utilization_deviation_pct",
                key=abs,
                ascending=False
            )
        )

        st.dataframe(
            flagged_display.round(2),
            use_container_width=True
        )

        st.warning("""
        **Important:** A flagged shop is not automatically fraudulent.
        It only indicates that its transaction/card behavior is
        significantly different from its peer cluster and requires
        further investigation.
        """)


# ============================================================
# TAB 3 — LOGISTICS OPTIMIZATION
# ============================================================

with tab3:

    st.header("🚚 Logistics Optimization")

    st.markdown("""
    **Objective:** Identify Portability Hubs that handle unusually
    high levels of non-local transactions and may therefore require
    more frequent stock replenishment.
    """)

    # --------------------------------------------------------
    # REQUIRED COLUMN
    # --------------------------------------------------------

    required = [
        "shopNo",
        "avg_portability"
    ]

    missing = [
        col
        for col in required
        if col not in shop_df.columns
    ]

    if missing:

        st.warning(
            f"Required columns are missing: {missing}"
        )

    else:

        logistics_df = shop_df.copy()

        # ----------------------------------------------------
        # PORTABILITY THRESHOLD
        # ----------------------------------------------------

        percentile = st.slider(
            "Portability Hub threshold percentile",
            min_value=70,
            max_value=99,
            value=90,
            step=5
        )

        threshold = logistics_df[
            "avg_portability"
        ].quantile(
            percentile / 100
        )

        # ----------------------------------------------------
        # IDENTIFY HUBS
        # ----------------------------------------------------

        logistics_df["portability_hub"] = np.where(
            logistics_df["avg_portability"] >= threshold,
            "Portability Hub",
            "Normal"
        )

        hubs = logistics_df[
            logistics_df["portability_hub"]
            == "Portability Hub"
        ]

        # ----------------------------------------------------
        # KPIs
        # ----------------------------------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Shops",
            len(logistics_df)
        )

        col2.metric(
            "Portability Hubs",
            len(hubs)
        )

        col3.metric(
            "Hub %",
            f"{len(hubs) / len(logistics_df) * 100:.2f}%"
        )

        # ----------------------------------------------------
        # TOP PORTABILITY SHOPS
        # ----------------------------------------------------

        st.subheader(
            "Top Portability Hubs"
        )

        top_hubs = (
            logistics_df
            .sort_values(
                "avg_portability",
                ascending=False
            )
            .head(20)
        )

        fig = px.bar(
            top_hubs,
            x="shopNo",
            y="avg_portability",
            color="cluster"
            if "cluster" in top_hubs.columns
            else None,
            title="Top 20 Portability Hubs"
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        # ----------------------------------------------------
        # HUB TABLE
        # ----------------------------------------------------

        display_cols = [
            "shopNo",
            "distName",
            "cluster",
            "avg_transactions",
            "avg_cards",
            "avg_portability",
            "avg_amount",
            "portability_hub"
        ]

        display_cols = [
            col
            for col in display_cols
            if col in hubs.columns
        ]

        st.dataframe(
            hubs[
                display_cols
            ].sort_values(
                "avg_portability",
                ascending=False
            ),
            use_container_width=True
        )

        # ----------------------------------------------------
        # BUSINESS INTERPRETATION
        # ----------------------------------------------------

        st.success("""
        **Logistics Recommendation:** Portability hubs should be
        prioritized for stock monitoring and potentially more frequent
        replenishment because they serve beneficiaries from outside
        their normal shop network.
        """)