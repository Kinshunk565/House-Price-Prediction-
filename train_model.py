"""
House Price Prediction — Model Training & Evaluation Pipeline
=============================================================
Trains three regression models, evaluates them, compares performance,
and saves the best model (Random Forest) for serving via Flask.
"""

import os
import json
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib

# ──────────────────────────────────────────────
# 1. DATA LOADING & EXPLORATION
# ──────────────────────────────────────────────
print("=" * 60)
print("  HOUSE PRICE PREDICTION — MODEL TRAINING PIPELINE")
print("=" * 60)

df = pd.read_csv("data/housing.csv")

print(f"\n📊 Dataset Shape: {df.shape}")
print(f"📋 Columns: {list(df.columns)}")
print(f"\n🔍 First 5 rows:\n{df.head()}")
print(f"\n📈 Statistical Summary:\n{df.describe()}")
print(f"\n❓ Missing Values:\n{df.isnull().sum()}")
print(f"\n🔄 Duplicates: {df.duplicated().sum()}")

# ──────────────────────────────────────────────
# 2. DATA PREPROCESSING
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  DATA PREPROCESSING")
print("=" * 60)

# Make a copy for processing
data = df.copy()

# Encode binary categorical columns (yes/no → 1/0)
binary_cols = ['mainroad', 'guestroom', 'basement',
               'hotwaterheating', 'airconditioning', 'prefarea']

for col in binary_cols:
    data[col] = data[col].map({'yes': 1, 'no': 0})

# Encode furnishing status
furnishing_encoder = LabelEncoder()
data['furnishingstatus'] = furnishing_encoder.fit_transform(data['furnishingstatus'])
print(f"   Furnishing classes: {list(furnishing_encoder.classes_)}")

# Encode location
location_encoder = LabelEncoder()
data['location'] = location_encoder.fit_transform(data['location'])
print(f"   Location classes: {list(location_encoder.classes_)}")

# ──────────────────────────────────────────────
# 3. FEATURE ENGINEERING
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  FEATURE ENGINEERING")
print("=" * 60)

# Create total_rooms feature
data['total_rooms'] = data['bedrooms'] + data['bathrooms']
print(f"   ✅ Created 'total_rooms' = bedrooms + bathrooms")

# Feature list (exclude target)
feature_cols = [
    'area', 'bedrooms', 'bathrooms', 'stories', 'mainroad',
    'guestroom', 'basement', 'hotwaterheating', 'airconditioning',
    'parking', 'prefarea', 'furnishingstatus', 'location',
    'property_age', 'total_rooms'
]

X = data[feature_cols]
y = data['price']

print(f"   Features ({len(feature_cols)}): {feature_cols}")
print(f"   Target: price")
print(f"   X shape: {X.shape}, y shape: {y.shape}")

# ──────────────────────────────────────────────
# 4. FEATURE SCALING
# ──────────────────────────────────────────────
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=feature_cols)

print(f"\n   ✅ Features scaled with StandardScaler")

# ──────────────────────────────────────────────
# 5. TRAIN-TEST SPLIT (80/20)
# ──────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

print(f"\n   Train set: {X_train.shape[0]} samples")
print(f"   Test set:  {X_test.shape[0]} samples")

# ──────────────────────────────────────────────
# 6. MODEL TRAINING & EVALUATION
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  MODEL TRAINING & EVALUATION")
print("=" * 60)

models = {
    'Linear Regression': LinearRegression(),
    'Decision Tree': DecisionTreeRegressor(max_depth=10, random_state=42),
    'Random Forest': RandomForestRegressor(
        n_estimators=200, max_depth=20, random_state=42, n_jobs=-1
    ),
}

results = {}

for name, model in models.items():
    print(f"\n{'─' * 40}")
    print(f"  Training: {name}")
    print(f"{'─' * 40}")

    # Train
    model.fit(X_train, y_train)

    # Predict
    y_pred = model.predict(X_test)

    # Metrics
    r2   = r2_score(y_test, y_pred)
    mae  = mean_absolute_error(y_test, y_pred)
    mse  = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)

    # Cross-validation (5-fold)
    cv_scores = cross_val_score(model, X_scaled, y, cv=5, scoring='r2')

    results[name] = {
        'r2':       round(r2, 4),
        'mae':      round(mae, 2),
        'mse':      round(mse, 2),
        'rmse':     round(rmse, 2),
        'cv_mean':  round(cv_scores.mean(), 4),
        'cv_std':   round(cv_scores.std(), 4),
    }

    print(f"   R² Score:    {r2:.4f}")
    print(f"   MAE:         ₹{mae:,.2f}")
    print(f"   MSE:         {mse:,.2f}")
    print(f"   RMSE:        ₹{rmse:,.2f}")
    print(f"   CV R² (5-fold): {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# ──────────────────────────────────────────────
# 7. MODEL COMPARISON TABLE
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  MODEL COMPARISON")
print("=" * 60)

comparison_df = pd.DataFrame(results).T
print(f"\n{comparison_df.to_string()}")

# Determine best model
best_model_name = max(results, key=lambda k: results[k]['r2'])
print(f"\n🏆 Best Model: {best_model_name} (R² = {results[best_model_name]['r2']})")

# ──────────────────────────────────────────────
# 8. FEATURE IMPORTANCE (Random Forest)
# ──────────────────────────────────────────────
rf_model = models['Random Forest']
importances = rf_model.feature_importances_
feature_importance = dict(zip(feature_cols, [round(float(x), 4) for x in importances]))

# Sort by importance
feature_importance = dict(
    sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
)

print("\n" + "=" * 60)
print("  FEATURE IMPORTANCE (Random Forest)")
print("=" * 60)
for feat, imp in feature_importance.items():
    bar = '█' * int(imp * 50)
    print(f"   {feat:20s} {imp:.4f} {bar}")

# ──────────────────────────────────────────────
# 9. SAVE MODELS & ARTIFACTS
# ──────────────────────────────────────────────
print("\n" + "=" * 60)
print("  SAVING MODELS & ARTIFACTS")
print("=" * 60)

os.makedirs('models', exist_ok=True)

# Save all trained models
for name, model in models.items():
    filename = name.lower().replace(' ', '_') + '.joblib'
    joblib.dump(model, f'models/{filename}')
    print(f"   ✅ Saved: models/{filename}")

# Save scaler & encoders
joblib.dump(scaler, 'models/scaler.joblib')
joblib.dump(furnishing_encoder, 'models/furnishing_encoder.joblib')
joblib.dump(location_encoder, 'models/location_encoder.joblib')
print(f"   ✅ Saved: scaler, furnishing_encoder, location_encoder")

# Save feature columns list
joblib.dump(feature_cols, 'models/feature_cols.joblib')

# Save metadata (metrics, feature importance, etc.)
metadata = {
    'model_results': results,
    'best_model': best_model_name,
    'feature_importance': feature_importance,
    'feature_columns': feature_cols,
    'locations': list(location_encoder.classes_),
    'furnishing_types': list(furnishing_encoder.classes_),
    'dataset_shape': list(df.shape),
    'price_stats': {
        'min': int(df['price'].min()),
        'max': int(df['price'].max()),
        'mean': int(df['price'].mean()),
        'median': int(df['price'].median()),
    }
}

with open('models/metadata.json', 'w') as f:
    json.dump(metadata, f, indent=2)
print(f"   ✅ Saved: models/metadata.json")

print("\n" + "=" * 60)
print("  ✅ TRAINING COMPLETE!")
print("=" * 60)
print(f"\n   Best model: {best_model_name}")
print(f"   R² Score:   {results[best_model_name]['r2']}")
print(f"   RMSE:       ₹{results[best_model_name]['rmse']:,.2f}")
print(f"\n   Run 'python app.py' to start the web server.\n")
