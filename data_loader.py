import pickle
import streamlit as st

from config import (
    SHOP_DF_PATH,
    MASTER_DF_PATH,
    SCALER_PATH,
    PCA_PATH,
    KMEANS_PATH,
    DBSCAN_PATH,
    FEATURES_PATH,
    CLUSTER_PROFILE_PATH
)


# ============================================================
# GENERIC PICKLE LOADER
# ============================================================

def load_pickle(path):

    with open(path, "rb") as f:
        return pickle.load(f)


# ============================================================
# SHOP DATA
# ============================================================

@st.cache_resource
def load_shop_df():

    return load_pickle(SHOP_DF_PATH)


# ============================================================
# MASTER DATA
# ============================================================

@st.cache_resource
def load_master_df():

    return load_pickle(MASTER_DF_PATH)


# ============================================================
# MODELS
# ============================================================

@st.cache_resource
def load_models():

    scaler = load_pickle(SCALER_PATH)

    pca = load_pickle(PCA_PATH)

    kmeans = load_pickle(KMEANS_PATH)

    dbscan = load_pickle(DBSCAN_PATH)

    features = load_pickle(FEATURES_PATH)

    return (
        scaler,
        pca,
        kmeans,
        dbscan,
        features
    )


# ============================================================
# CLUSTER PROFILE
# ============================================================

@st.cache_resource
def load_cluster_profile():

    return load_pickle(CLUSTER_PROFILE_PATH)