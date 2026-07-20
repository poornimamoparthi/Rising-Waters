import os
import numpy as np
import pandas as pd

def generate_flood_data(num_samples=1450, random_seed=42):
    np.random.seed(random_seed)
    
    annual_rainfall = np.random.normal(loc=2200, scale=600, size=num_samples)
    annual_rainfall = np.clip(annual_rainfall, 800, 4500)
    
    seasonal_fraction = np.random.uniform(0.65, 0.80, size=num_samples)
    seasonal_rainfall = annual_rainfall * seasonal_fraction + np.random.normal(0, 100, size=num_samples)
    seasonal_rainfall = np.clip(seasonal_rainfall, 500, 3500)
    
    cloud_visibility = 10.0 - (seasonal_rainfall / 400.0) + np.random.normal(0, 1.2, size=num_samples)
    cloud_visibility = np.clip(cloud_visibility, 0.0, 10.0)
    
    temperature = np.random.normal(loc=28, scale=4, size=num_samples)
    temperature = np.clip(temperature, 15, 42)
    
    humidity = 50.0 + (seasonal_rainfall / 60.0) + np.random.normal(0, 5, size=num_samples)
    humidity = np.clip(humidity, 45.0, 100.0)
    
    wind_speed = np.random.normal(loc=18, scale=7, size=num_samples)
    wind_speed = np.clip(wind_speed, 3, 50)
    
    pressure = 1015.0 - (seasonal_rainfall / 300.0) + np.random.normal(0, 3, size=num_samples)
    pressure = np.clip(pressure, 985.0, 1025.0)
    
    weather_conditions = []
    for sr in seasonal_rainfall:
        if sr > 2200:
            cond = np.random.choice(['Rainy', 'Overcast'], p=[0.7, 0.3])
        elif sr > 1400:
            cond = np.random.choice(['Rainy', 'Overcast', 'Cloudy'], p=[0.4, 0.4, 0.2])
        elif sr > 900:
            cond = np.random.choice(['Cloudy', 'Overcast', 'Sunny'], p=[0.5, 0.2, 0.3])
        else:
            cond = np.random.choice(['Sunny', 'Cloudy'], p=[0.8, 0.2])
        weather_conditions.append(cond)
    
    norm_annual = (annual_rainfall - 800) / 3700
    norm_seasonal = (seasonal_rainfall - 500) / 3000
    norm_humidity = (humidity - 45) / 55
    norm_visibility = (10 - cloud_visibility) / 10
    norm_pressure = (1025 - pressure) / 40
    
    flood_score = (
        0.35 * norm_seasonal + 
        0.25 * norm_annual + 
        0.15 * norm_humidity + 
        0.15 * norm_visibility + 
        0.10 * norm_pressure + 
        np.random.normal(0, 0.012, size=num_samples)
    )
    
    threshold = np.percentile(flood_score, 68)
    flood_chance = (flood_score >= threshold).astype(int)
    
    df = pd.DataFrame({
        'Annual_Rainfall': annual_rainfall,
        'Seasonal_Rainfall': seasonal_rainfall,
        'Cloud_Visibility': cloud_visibility,
        'Temperature': temperature,
        'Humidity': humidity,
        'Wind_Speed': wind_speed,
        'Pressure': pressure,
        'Weather_Condition': weather_conditions,
        'Flood_Chance': flood_chance
    })
    
    nan_mask_vis = np.random.choice([True, False], size=num_samples, p=[0.015, 0.985])
    nan_mask_temp = np.random.choice([True, False], size=num_samples, p=[0.015, 0.985])
    
    df.loc[nan_mask_vis, 'Cloud_Visibility'] = np.nan
    df.loc[nan_mask_temp, 'Temperature'] = np.nan
    
    outlier_indices_rain = np.random.choice(num_samples, size=5, replace=False)
    outlier_indices_temp = np.random.choice(num_samples, size=5, replace=False)
    
    df.loc[outlier_indices_rain, 'Annual_Rainfall'] = df.loc[outlier_indices_rain, 'Annual_Rainfall'] * 2.5
    df.loc[outlier_indices_temp, 'Temperature'] = df.loc[outlier_indices_temp, 'Temperature'] + 20.0
    
    os.makedirs('data', exist_ok=True)
    
    df.to_csv('data/flood_data.csv', index=False)
    print(f"Dataset generated successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
    print(f"Missing values introduced: Cloud_Visibility ({df['Cloud_Visibility'].isna().sum()}), Temperature ({df['Temperature'].isna().sum()})")
    print(f"Target distribution (Flood_Chance):\n{df['Flood_Chance'].value_counts(normalize=True)}")

if __name__ == '__main__':
    generate_flood_data()
