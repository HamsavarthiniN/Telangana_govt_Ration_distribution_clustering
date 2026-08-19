import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Telangana Ration Shop Analytics",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# PAGE DEFINITIONS
# ============================================================

overview = st.Page(
    "pages/1_Overview.py",
    title="Overview",
    icon="📊",
    url_path="overview"
)

cluster_analysis = st.Page(
    "pages/2_Cluster_Analysis.py",
    title="Cluster Analysis",
    icon="🔵",
    url_path="cluster-analysis"
)

shop_explorer = st.Page(
    "pages/3_Shop_Explorer.py",
    title="Shop Explorer",
    icon="🏪",
    url_path="shop-explorer"
)

geospatial_hotspots = st.Page(
    "pages/4_Geospatial_Hotspots.py",
    title="Geospatial Hotspots",
    icon="🗺️",
    url_path="geospatial-hotspots"
)

anomaly_detection = st.Page(
    "pages/5_Anomaly_Detection.py",
    title="Anomaly Detection",
    icon="⚠️",
    url_path="anomaly-detection"
)

policy_business_insights = st.Page(
    "pages/6_Policy_Business_Insights.py",
    title="Policy & Business Insights",
    icon="📈",
    url_path="policy-business-insights"
)


# ============================================================
# NAVIGATION
# ============================================================

pg = st.navigation(
    {
        "Dashboard": [
            overview,
            cluster_analysis,
            shop_explorer,
            geospatial_hotspots,
            anomaly_detection,
            policy_business_insights
        ]
    },
    position="sidebar"
)


# ============================================================
# SIDEBAR INFORMATION
# ============================================================

with st.sidebar:

    st.markdown("---")

    st.markdown(
        """
        ### 🏪 Telangana Ration Analytics

        **Fair Price Shop Distribution**

        Analyze:

        • Shop performance  
        • Behavioral clusters  
        • Geospatial hotspots  
        • Anomalies  
        • Policy impact  
        • Business insights
        """
    )

    st.markdown("---")


# ============================================================
# RUN SELECTED PAGE
# ============================================================

pg.run()