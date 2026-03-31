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
scaler = joblib.load('models/scaler.joblib')
furnishing_encoder = joblib.load('models/furnishing_encoder.joblib')
location_encoder = joblib.load('models/location_encoder.joblib')
feature_cols = joblib.load('models/feature_cols.joblib')

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

        # Calculate confidence range (±8%)
        lower_bound = prediction * 0.92
        upper_bound = prediction * 1.08

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
            }
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
