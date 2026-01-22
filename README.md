# 🇿🇦 The Brazilians: Scouting Intelligence Lab
### *AI-Powered Performance Twin Finder for Elite South African Football*

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-Framework-FF4B4B.svg)
![Scikit-Learn](https://img.shields.io/badge/Machine_Learning-SKLearn-orange.svg)

## ⚽ Project Overview
The **Scouting Intelligence Lab** is a high-performance analytics tool designed to identify "Performance Twins" for elite footballers. Using a K-Nearest Neighbors (KNN) algorithm, the system analyzes performance DNA to find players who match the statistical profile of a benchmark player (e.g., Themba Zwane or Teboho Mokoena).

This tool bridges the gap between raw data and technical recruitment, allowing scouts to weight specific metrics—like assist importance—to align with a club's tactical philosophy.



## 🚀 Key Features
* **KNN Similarity Engine:** Uses Cosine Similarity to find the closest statistical matches in a multi-dimensional feature space.
* **Performance DNA (Radar Charts):** Interactive visualization comparing a benchmark player against a scouted "twin."
* **Match Strength Score:** A percentage-based similarity score (0-100%) to quantify the accuracy of the match.
* **Custom Importance Weighting:** Adjust the influence of specific metrics (like Assists) to find different types of players.
* **Automated Scouting Reports:** Export findings into professional CSV formats for the technical team.

## 🛠️ The Tech Stack
* **Frontend:** [Streamlit](https://streamlit.io/) (Custom CSS for Sundowns/Elite Branding)
* **Data Science:** [Pandas](https://pandas.pydata.org/) & [Scikit-learn](https://scikit-learn.org/)
* **Visualization:** [Plotly](https://plotly.com/)
* **Algorithm:** K-Nearest Neighbors (Metric: Cosine)

## 📊 How it Works
1. **Feature Selection:** We analyze Goals, Assists, Shots, Shot Accuracy %, and Goals per Shot.
2. **Standardization:** All data is scaled using `StandardScaler` to ensure fair comparison across different units.
3. **Distance Calculation:** The model calculates the "distance" between players in a 5-dimensional space.
4. **Scouting Result:** The closest 5 players are returned as "Performance Twins."

## 🏗️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/your-username/sundowns-scout-ai.git](https://github.com/your-username/sundowns-scout-ai.git)
