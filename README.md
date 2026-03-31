<div align="center">
  
# 🏢 Kinshuk Garg | Neural Estate Intelligence

**Institutional-Grade Real Estate Valuation Powered by Machine Learning**

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg?style=for-the-badge&logo=python)](https://www.python.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-%23F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Live on Render](https://img.shields.io/badge/Live_Demo-Render-46E3B7.svg?style=for-the-badge&logo=render&logoColor=white)](https://kinshuk-intelligence.onrender.com/)

</div>

<br/>

## 📖 Overview

**Neural Estate Intelligence** is a high-end predictive machine learning web application. It is designed to compute highly accurate real estate valuations for luxury properties across India's most premium hubs.

By applying **high-dimensional Random Forest topology** across 1,200 curated property records, the algorithm neutralizes market noise to deliver institutional-grade price predictions. This computational engine is wrapped in a breathtaking **animated dark-mode glassmorphic UI**, designed to emulate a quantitative algorithmic trading terminal.

---

## ✨ Key Features

- **🎯 High-Fidelity Machine Learning:** Built on a robust `RandomForestRegressor` trained on 15 dimensional vectors (Area, Age, Location, Bathrooms, etc.) securing up to **~85% R² variance accuracy**.
- **🌌 Futuristic Dark-Mode UI:** A hand-crafted, fully responsive web interface featuring deep black canvases, frosted glass panels (`backdrop-filter`), and glowing neon-white accents.
- **🎬 Cinematic Animations:** Immersive user experience with 3D hovering cards (`vanilla-tilt.js`), slot-machine price counters, intersection-observer wipe-ins, and dynamic scanner borders.
- **🗺️ Extensive Geographic Tracking:** Supports predictive modeling across **25+ premium Indian hubs** including *South Mumbai, Vasant Vihar, Jubilee Hills, Koramangala, Boat Club,* and *Koregaon Park*.
- **📊 Real-Time Matrix Telemetry:** The interface dynamically exposes underlying algorithm statistics in real-time, displaying MAE, RMSE, Cross-Validation Scores, and dynamic Feature Importance tracking.

<br/>

## 🛠️ Tech Stack

### Frontend (UI/UX)
* **Design Pattern:** Glassmorphism, Deep Space Dark Theme
* **Languages:** HTML5, modern CSS3, Vanilla JavaScript (ES6+)
* **Libraries:** `Vanilla-tilt.js` (for interactive 3D card physics)
* **Typography:** `Space Grotesk` Google Font

### Backend (Server & API)
* **Framework:** Python Flask (`flask`, `flask-cors`)
* **Architecture:** RESTful JSON endpoints architecture

### Data Science & Machine Learning
* **Algorithms:** Scikit-Learn (Random Forest, Decision Trees, Linear Regression)
* **Data Processing:** Pandas, NumPy
* **Serialization:** Joblib (for model & scaler persistence)

<br/>

## 🚀 Installation Guide

Follow these steps to deploy the Neural Environment on your local machine.

### 1. Clone the Repository
```bash
git clone https://github.com/Kinshunk565/House-Price-Prediction-.git
cd House-Price-Prediction-
```

### 2. Set Up Virtual Environment
Create an isolated Python environment to avoid global dependency issues.

**Windows:**
```cmd
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask flask-cors pandas numpy scikit-learn joblib
```

### 4. Boot the Engine
Start up the Flask server to host the web interface and the predictive API.
```bash
python app.py
```

### 5. Access the Terminal
You can access the live, publicly deployed model here:  
👉 **[https://kinshuk-intelligence.onrender.com/](https://kinshuk-intelligence.onrender.com/)**

Or if you are running it locally on your machine, navigate to:  
👉 **http://localhost:5000**

<br/>

## 🧠 Algorithmic Execution Flow (How it Works)

1. **The Pulse**: The UI packages your selected configurations (Area, Age, Zip Code, Amenities) into a secure JSON payload and sends a `POST` request to `/predict`.
2. **Preprocessing Matrix**: The Python API receives the request. Categorical data (like location name) is instantly encoded into vectors via `LabelEncoder`. The full array is heavily normalized via the `StandardScaler`.
3. **Inference Compute**: A matrix of 200 individual decision trees (`n_estimators=200` in the Random Forest) runs parallel splits over your property blueprint to aggregate a final consensus.
4. **The Verdict**: A calculated confidence bound (±1.5%) is mapped alongside the raw prediction and streamed immediately back to the frontend.
5. **Telemetry Render**: JavaScript intercepts the numeric array, scrambles the characters on screen for a "calculating" aesthetic, and locks into the final formatted ₹ INR valuation output.

---

<div align="center">
    <p>Constructed by <b>Kinshuk Garg</b> • All models strictly for demonstration purposes.</p>
</div>