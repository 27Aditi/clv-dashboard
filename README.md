# Customer Lifetime Value (CLV) Dashboard

An interactive Customer Lifetime Value (CLV) analytics dashboard built using Streamlit.  
This project analyzes customer behavior, segments users based on value, and visualizes
key CLV metrics to support data-driven business decisions.

---

## Problem Statement

Understanding customer lifetime value is crucial for improving retention, targeting
high-value customers, and optimizing marketing strategies. Raw transactional data alone
does not provide actionable insights without proper analysis and visualization.

---

## Solution Overview

This dashboard processes customer transaction data, computes CLV-related metrics, and
segments customers into meaningful categories. The results are presented through
interactive charts and KPIs that help stakeholders quickly interpret customer value trends.

---

## Key Features

- Customer-wise and segment-wise CLV analysis
- Interactive visualizations using Plotly
- Cleaned and optimized datasets stored in Parquet format
- Fast and scalable Streamlit dashboard
- Consistent UI styling using Streamlit configuration

---

## Tech Stack

- Python
- Pandas
- PyArrow
- Matplotlib
- Seaborn
- Plotly
- Streamlit

---

## Project Structure

## Project Structure

```text
clv_dashboard/
│
├── .streamlit/
│   └── config.toml          # Streamlit UI and theme configuration
│
├── data/                    # Raw CSV datasets
│   ├── dataset1.csv
│   └── dataset2.csv
│
├── processed_data/          # Cleaned and optimized datasets
│   ├── customer_wise.parquet
│   └── segment_wise.parquet
│
├── app.py                   # Streamlit dashboard application
├── requirements.txt         # Project dependencies
└── README.md                # Project documentation
```
---

## How to Run Locally

1. Clone the repository
2. Install dependencies:
   pip install -r requirements.txt
3. Run the Streamlit app:
   streamlit run app.py

---

## Live Application

https://dashboardclv.streamlit.app/

---

## Author

Aditi Bhatnagar  
Computer Science Engineering | Data Science & Machine Learning Enthusiast
