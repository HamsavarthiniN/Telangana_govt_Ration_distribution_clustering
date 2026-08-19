# Telangana Government Ration Distribution Analysis, Behavioral Clustering & Anomaly Detection

## Project Objective

This project analyzes Telangana Government Fair Price Shop (FPS) data using machine learning to:

- Segment shops based on operational behavior using **K-Means clustering**.
- Identify unusual shop behavior using **DBSCAN**.
- Analyze geographical distribution of shop clusters.
- Analyze portability trends and identify **Portability Hubs**.
- Identify shops requiring further review based on transaction-to-card behavior.
- Support logistics and operational planning through an interactive **Streamlit dashboard**.

---

## Project Structure

```text
Telangana_govt_Ration_distribution_clustering/
│
├── app.py
├── data_loader.py
├── config.py
│
├── pages/
│   ├── 1_Overview.py
│   ├── 2_Cluster_Analysis.py
│   ├── 3_Shop_Explorer.py
│   ├── 4_Geospatial_Hotspots.py
│   ├── 5_Anomaly_Detection.py
│   └── 6_Policy_Business_Insights.py
│
├── feature_dataset.pkl
├── master_dataset_cleaned.pkl
├── scaler.pkl
├── pca.pkl
├── kmeans.pkl
├── dbscan.pkl
├── features.pkl
└── cluster_profile.pkl
---
## Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Plotly
- Streamlit

---

## Models Used

### Shop Behavioral Segmentation

**K-Means Clustering** — used to group shops into 5 behavioral clusters based on their operational features.

### Anomaly Detection

**DBSCAN** — used to identify shops with unusual behavioral patterns and classify them as noise/anomaly candidates.

### Dimensionality Reduction

**PCA** — used for dimensionality reduction and visualization of the shop-level feature space.

---

## Setup Instructions

1. **Clone the Repository**-git clone https://github.com/HamsavarthiniN/Telangana_govt_Ration_distribution_clustering.git
2. **Create a Virtual Environment**- python -m venv myenv
   - *Activate-Windows*-copy path of Activate.ps1 and paste in terminal  
4. **Install Dependencies**- pip install -r requirements.txt
5. **Run the Streamlit Dashboard**-streamlit run app.py
