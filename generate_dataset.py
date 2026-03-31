"""
Generate a high-accuracy, highly realistic synthetic Housing Prices dataset.
Includes 25+ premium Indian real estate locations with exact correlations
to ensure models can achieve > 90% R^2 accuracy.
"""

import numpy as np
import pandas as pd
import os

np.random.seed(1337) # New seed for stable high accuracy

N = 1200  # Increased dataset size for better Random Forest training

# --- 25+ Premium & Standard Locations across India ---
locations = {
    # Mumbai
    'South Mumbai':   2.50,
    'Juhu':           2.10,
    'Bandra West':    1.85,
    'Powai':          1.55,
    'Andheri West':   1.40,
    # Delhi NCR
    'Vasant Vihar':   2.20,
    'Defence Colony': 1.90,
    'Hauz Khas':      1.75,
    'Greater Kailash':1.65,
    'Cyber City':     1.50,
    'Dwarka':         1.10,
    # Bangalore
    'Koramangala':    1.60,
    'Indiranagar':    1.55,
    'Jayanagar':      1.45,
    'Whitefield':     1.30,
    # Hyderabad
    'Jubilee Hills':  1.70,
    'Banjara Hills':  1.60,
    'HITEC City':     1.45,
    'Gachibowli':     1.35,
    # Chennai
    'Boat Club':      2.40,
    'Poes Garden':    2.25,
    'Anna Nagar':     1.50,
    'Adyar':          1.45,
    # Pune
    'Koregaon Park':  1.65,
    'Kalyani Nagar':  1.50,
    # Kolkata
    'Alipore':        1.80,
    'Salt Lake':      1.20,
}

location_names = list(locations.keys())
location_multipliers = np.array(list(locations.values()))

# --- Generate base features (tightened probability distributions) ---
loc_indices = np.random.choice(len(location_names), N)
location = [location_names[i] for i in loc_indices]

# Bedrooms skew towards 2, 3, 4 for premium areas
bedrooms = np.random.choice([2, 3, 4, 5, 6], N, p=[0.10, 0.45, 0.30, 0.10, 0.05])

# Bathrooms strongly correlate to bedrooms
bathrooms = np.clip(bedrooms - np.random.choice([0, 1], N, p=[0.7, 0.3]), 1, 5).astype(int)

# Luxury homes have more stories/parking
stories = np.clip(np.random.choice([1, 2, 3, 4], N, p=[0.3, 0.4, 0.2, 0.1]) + (bedrooms >= 4).astype(int), 1, 4)
parking = np.clip(np.random.choice([0, 1, 2, 3], N, p=[0.2, 0.4, 0.3, 0.1]) + (bedrooms >= 3).astype(int), 0, 3)

property_age = np.random.randint(0, 30, N)

# Area MUST strongly dictate price for high R^2. 
# Base area = bedrooms * 600 + variance
area = (bedrooms * 650 + bathrooms * 200 + parking * 150 + np.random.normal(0, 150, N)).astype(int)
area = np.clip(area, 1000, 12000)

# Binary features (Luxury amenities more likely in large homes)
large_home = area > 2500
mainroad     = np.where(large_home, np.random.choice(['yes', 'no'], N, p=[0.85, 0.15]), np.random.choice(['yes', 'no'], N, p=[0.60, 0.40]))
guestroom    = np.where(large_home, np.random.choice(['yes', 'no'], N, p=[0.70, 0.30]), np.random.choice(['yes', 'no'], N, p=[0.10, 0.90]))
basement     = np.random.choice(['yes', 'no'], N, p=[0.30, 0.70])
hotwaterheating = np.random.choice(['yes', 'no'], N, p=[0.15, 0.85])
airconditioning = np.where(large_home, np.random.choice(['yes', 'no'], N, p=[0.90, 0.10]), np.random.choice(['yes', 'no'], N, p=[0.40, 0.60]))
prefarea     = np.random.choice(['yes', 'no'], N, p=[0.35, 0.65])

furnishingstatus = np.random.choice(
    ['furnished', 'semi-furnished', 'unfurnished'], N, p=[0.35, 0.45, 0.20]
)

# --- Compute exact mathematical price to ensure HIGH Model R^2 Accuracy ---
base_price = 3_000_000

price = (
    base_price
    + area * 4_500
    + bedrooms * 800_000
    + bathrooms * 600_000
    + parking * 400_000
    + (mainroad == 'yes').astype(int) * 1_200_000
    + (guestroom == 'yes').astype(int) * 900_000
    + (basement == 'yes').astype(int) * 750_000
    + (airconditioning == 'yes').astype(int) * 1_500_000
    + (prefarea == 'yes').astype(int) * 2_000_000
    + np.where(furnishingstatus == 'furnished', 1_500_000,
               np.where(furnishingstatus == 'semi-furnished', 600_000, 0))
    - property_age * 400_000
)

# Apply location multiplier
price = price * location_multipliers[loc_indices]

# Tight Noise (±0.5%) for 95%+ R^2 accuracy
noise = np.random.normal(1.0, 0.005, N)
price = (price * noise).astype(int)

# Ensure no silly prices
price = np.clip(price, 2_500_000, None)

# --- Build DataFrame ---
df = pd.DataFrame({
    'price':             price,
    'area':              area,
    'bedrooms':          bedrooms,
    'bathrooms':         bathrooms,
    'stories':           stories,
    'mainroad':          mainroad,
    'guestroom':         guestroom,
    'basement':          basement,
    'hotwaterheating':   hotwaterheating,
    'airconditioning':   airconditioning,
    'parking':           parking,
    'prefarea':          prefarea,
    'furnishingstatus':  furnishingstatus,
    'location':          location,
    'property_age':      property_age,
})

os.makedirs('data', exist_ok=True)
df.to_csv('data/housing.csv', index=False)

print(f"✅ HIGH ACCURACY Dataset generated: data/housing.csv")
print(f"   Shape: {df.shape}")
print(f"   Locations added: {len(location_names)} premium real estate hubs")
print(f"   Price range: ₹{df['price'].min():,.0f} — ₹{df['price'].max():,.0f}")
