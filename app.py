"""
House Price Prediction — Flask Web Server
==========================================
Serves the web interface and provides REST API endpoints
for real-time house price predictions.
"""

import json
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
CORS(app)

# ──────────────────────────────────────────────
# LOAD MODEL & ARTIFACTS
# ──────────────────────────────────────────────
print("🔄 Loading model artifacts...")

rf_model = joblib.load('models/random_forest.joblib')
lr_model = joblib.load('models/linear_regression.joblib') # For XAI Breakdown
scaler = joblib.load('models/scaler.joblib')
furnishing_encoder = joblib.load('models/furnishing_encoder.joblib')
location_encoder = joblib.load('models/location_encoder.joblib')
feature_cols = joblib.load('models/feature_cols.joblib')

# Load the historical dataset for Market Computables (KNN simulation)
try:
    historical_df = pd.read_csv('data/housing.csv')
except:
    historical_df = pd.DataFrame() # Fallback

with open('models/metadata.json', 'r') as f:
    metadata = json.load(f)

print("✅ Model loaded successfully!")

# ──────────────────────────────────────────────
# ROUTES
# ──────────────────────────────────────────────

@app.route('/')
def index():
    """Serve the main web interface."""
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """Accept property features and return price prediction."""
    try:
        data = request.get_json()

        # Extract features from request
        area = float(data.get('area', 3000))
        bedrooms = int(data.get('bedrooms', 3))
        bathrooms = int(data.get('bathrooms', 2))
        stories = int(data.get('stories', 2))
        mainroad = int(data.get('mainroad', 1))
        guestroom = int(data.get('guestroom', 0))
        basement = int(data.get('basement', 0))
        hotwaterheating = int(data.get('hotwaterheating', 0))
        airconditioning = int(data.get('airconditioning', 0))
        parking = int(data.get('parking', 1))
        prefarea = int(data.get('prefarea', 0))
        furnishingstatus = data.get('furnishingstatus', 'semi-furnished')
        location = data.get('location', 'Whitefield')
        property_age = int(data.get('property_age', 5))

        # Encode categorical features
        furnishing_encoded = furnishing_encoder.transform([furnishingstatus])[0]
        location_encoded = location_encoder.transform([location])[0]

        # Compute engineered features
        total_rooms = bedrooms + bathrooms

        # Build feature vector in correct order
        feature_values = [
            area, bedrooms, bathrooms, stories, mainroad,
            guestroom, basement, hotwaterheating, airconditioning,
            parking, prefarea, furnishing_encoded, location_encoded,
            property_age, total_rooms
        ]

        # Create DataFrame with feature names
        feature_df = pd.DataFrame([feature_values], columns=feature_cols)

        # Scale features
        feature_scaled = scaler.transform(feature_df)

        # Predict
        prediction = rf_model.predict(feature_scaled)[0]

        # ──────────────────────────────────────────────
        # XAI (Explainable AI) Breakdown 
        # ──────────────────────────────────────────────
        # We use the Linear Regression model intercepts and coefficients to proxy the Black-Box Random Forest for the UI
        base_price = float(lr_model.intercept_)
        waterfall = [{'feature': 'Base Value', 'impact': round(base_price)}]
        
        for idx, col in enumerate(feature_cols):
            val_impact = float(feature_scaled[0][idx] * lr_model.coef_[idx])
            if abs(val_impact) > 500000: # Only show significant impacts (>5L)
                waterfall.append({
                    'feature': col,
                    'impact': round(val_impact)
                })

        # ──────────────────────────────────────────────
        # MARKET COMPARABLES (Comps)
        # ──────────────────────────────────────────────
        comps = []
        if not historical_df.empty:
            # Filter to same location and similar size, then sort by absolute area distance
            loc_df = historical_df[historical_df['location'] == location].copy()
            if loc_df.empty:
                loc_df = historical_df.copy() # fallback to all if location anomaly
            
            loc_df['area_dist'] = abs(loc_df['area'] - area)
            loc_df = loc_df.sort_values(by='area_dist').head(3)
            
            for _, row in loc_df.iterrows():
                comps.append({
                    'price': f"₹{row['price']:,.0f}",
                    'area': f"{row['area']} Sq.Ft",
                    'bedrooms': row['bedrooms'],
                    'bathrooms': row['bathrooms'],
                    'location': row['location'].upper()
                })

        return jsonify({
            'success': True,
            'predicted_price': round(float(prediction)),
            'price_range': {
                'low': round(float(lower_bound)),
                'high': round(float(upper_bound)),
            },
            'formatted_price': f"₹{prediction:,.0f}",
            'formatted_range': {
                'low': f"₹{lower_bound:,.0f}",
                'high': f"₹{upper_bound:,.0f}",
            },
            'xai_breakdown': waterfall,
            'comparables': comps
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/model-info', methods=['GET'])
def model_info():
    """Return model comparison metrics and feature importances."""
    return jsonify({
        'success': True,
        'model_results': metadata['model_results'],
        'best_model': metadata['best_model'],
        'feature_importance': metadata['feature_importance'],
        'price_stats': metadata['price_stats'],
        'dataset_shape': metadata['dataset_shape'],
    })


@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Return list of valid locations."""
    return jsonify({
        'success': True,
        'locations': metadata['locations'],
        'furnishing_types': metadata['furnishing_types'],
    })


# ──────────────────────────────────────────────
# RUN SERVER
# ──────────────────────────────────────────────
if __name__ == '__main__':
    print("\n🏠 House Price Prediction Server")
    print("   URL: http://localhost:5000")
    print("   Press Ctrl+C to stop.\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
