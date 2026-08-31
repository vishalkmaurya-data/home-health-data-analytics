# 🏥 Home Health Care Analytics & Provider Risk Intelligence

> 📊 **An end-to-end Data Analytics & Business Intelligence project for analyzing Home Health Care provider performance, Medicare payments, patient volume, clinical risk, geographic patterns, and provider-level risk.**

[![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)](https://plotly.com/)
[![GitHub](https://img.shields.io/badge/GitHub-Repository-181717?logo=github&logoColor=white)](https://github.com/)

---

## 🚀 Live Dashboard

### 🌐 Interactive Streamlit Dashboard

👉 **[Open Live Dashboard](https://home-health-data-analytics-cteciwuhzos7gjb8dkhqev.streamlit.app/)**

> Explore provider performance, financial metrics, geographic patterns, operational KPIs, and provider risk interactively.

---

# 📌 Project Overview

The **Home Health Care Analytics & Provider Risk Intelligence** project transforms provider-level healthcare data into an interactive Business Intelligence dashboard.

The project combines:

- 🧹 Data Cleaning
- 🔍 Exploratory Data Analysis
- 📊 Statistical Analysis
- 💰 Medicare Payment Analysis
- 🏥 Provider Performance Analysis
- 👥 Beneficiary & Episode Analysis
- 🗺️ Geographic Analysis
- 🩺 Clinical Risk Analysis
- ⚠️ Provider Risk Scoring
- 📈 Interactive Dashboard Development

The final analytical dataset contains:

**100,000 provider-level records and 62 analytical features before the final dashboard presentation layer.**

---

# 🎯 Business Problem

Healthcare organizations manage a large number of providers with significant differences in:

- Patient volume
- Number of episodes
- Medicare payments
- Service utilization
- Beneficiary characteristics
- Clinical risk
- Geographic distribution
- Provider-level operational performance

A business manager needs a way to quickly identify:

> **Which providers generate the highest financial activity, which regions contribute the most volume, and which providers require additional risk attention?**

This project addresses that problem through an interactive analytical dashboard.

---

# 💡 Business Objectives

The project focuses on answering important business questions:

### 💰 Financial Performance

- How much Medicare payment is associated with the provider network?
- How do Medicare payments compare with submitted charges?
- Which states generate the highest Medicare payment volume?
- Which providers have unusual payment patterns?

### 🏥 Provider Performance

- Which providers handle the highest number of episodes?
- Which providers serve the largest beneficiary populations?
- Which providers have the highest risk scores?
- How does provider activity differ across locations?

### 👥 Operational Analysis

- How many episodes are associated with beneficiaries?
- What is the relationship between episodes and beneficiaries?
- How do visit metrics vary across providers?

### 🩺 Clinical Risk

- What is the average HCC score?
- What is the average beneficiary age?
- How prevalent are major clinical conditions?
- How does clinical risk relate to provider-level risk?

### ⚠️ Risk Intelligence

- Which providers fall into High, Medium, and Low risk categories?
- Where are high-risk providers concentrated?
- Which providers should receive additional business attention?

---

# 📊 Dataset Summary

| Metric | Value |
|---|---:|
| 📋 Final Records | **100,000** |
| 📊 Analytical Columns | **62** |
| 🏥 Unique Provider Records | **100,000** |
| 🏢 Agencies | **9,588** |
| 🧾 Total Episodes | **55.16M** |
| 👥 Total Beneficiaries | **31.95M** |
| 💵 Total HHA Charges | **$167.34B** |
| 💳 Total Medicare Payments | **$163.84B** |
| ⚠️ High-Risk Providers | **33,334** |
| 📈 Average Risk Score | **0.5001** |

---

# 🧹 Data Preparation & Quality

The project includes a complete data preparation workflow.

### 🔹 Data Cleaning

The raw provider dataset was processed through multiple validation stages:

```text
Raw Data
   ↓
Data Type Validation
   ↓
Missing Value Analysis
   ↓
Missing Value Treatment
   ↓
Duplicate Detection
   ↓
Logical Validation
   ↓
Outlier Inspection
   ↓
Risk Target Creation
   ↓
Synthetic Dataset Generation
   ↓
Final Data Quality Validation
   ↓
Dashboard-Ready Dataset
