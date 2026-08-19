# Telangana Government Ration Distribution Analysis, Behavioral Clustering & Anomaly Detection

## 📌 Project Objective

This project analyzes **Telangana Government Fair Price Shop (FPS)** data using machine learning techniques to:

- Segment shops based on operational behavior using **K-Means clustering**.  
- Detect unusual shop behavior using **DBSCAN**.  
- Examine the **geographical distribution** of shop clusters.  
- Analyze portability trends and identify **Portability Hubs**.  
- Flag shops requiring further review based on **transaction-to-card behavior**.  
- Support logistics and operational planning through an interactive **Streamlit dashboard**.  

---

## 📂 Project Structure

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
```
## 📊 Dataset Access

The master dataset (`master_dataset_cleaned.csv` / `.pkl`) is **not included in this repository** due to size limitations.  
Please download it from Google Drive before running the project:

👉 [Download Dataset from Google Drive]((https://drive.google.com/drive/folders/1wOfSib8fuDFQM2DwZu54QwAxyT1gTtwa?usp=drive_link))

After downloading, place the dataset in the project root folder:
---

## ⚙️ Technologies Used

- **Python**  
- **Pandas**  
- **NumPy**  
- **Scikit-learn**  
- **Matplotlib**  
- **Plotly**  
- **Streamlit**  

---

## 🤖 Models Used

### Shop Behavioral Segmentation
- **K-Means Clustering** — groups shops into **5 behavioral clusters** based on operational features.

### Anomaly Detection
- **DBSCAN** — identifies shops with unusual behavioral patterns and classifies them as **noise/anomaly candidates**.

### Dimensionality Reduction
- **PCA** — reduces dimensionality and enables visualization of the shop-level feature space.

---

## 🚀 Setup Instructions

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/HamsavarthiniN/Telangana_govt_Ration_distribution_clustering.git
   ```

2. **Create a Virtual Environment**  
   ```bash
   python -m venv myenv
   ```
   - **Activate (Windows)**: Copy the path of `Activate.ps1` and paste it into the terminal.

3. **Install Dependencies**  
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit Dashboard**  
   ```bash
   streamlit run app.py
