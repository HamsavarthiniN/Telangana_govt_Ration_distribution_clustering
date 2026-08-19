from pathlib import Path


# ============================================================
# BASE PROJECT DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


# ============================================================
# DATA FILES
# ============================================================

SHOP_DF_PATH = BASE_DIR / "shop_df.pkl"

MASTER_DF_PATH = BASE_DIR / "master_dataset_cleaned.pkl"


# ============================================================
# MODEL FILES
# ============================================================

SCALER_PATH = BASE_DIR / "scaler.pkl"

PCA_PATH = BASE_DIR / "pca.pkl"

KMEANS_PATH = BASE_DIR / "kmeans.pkl"

DBSCAN_PATH = BASE_DIR / "dbscan.pkl"

FEATURES_PATH = BASE_DIR / "features.pkl"


# ============================================================
# ANALYSIS OUTPUTS
# ============================================================

CLUSTER_PROFILE_PATH = BASE_DIR / "cluster_profile.pkl"