import os
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'flood_prediction_secret_key_for_session_management'

MODEL_PATH = 'floods.save'

if os.path.exists(MODEL_PATH):
    print(f"Loading model and scaler from '{MODEL_PATH}'...")
    model_data = joblib.load(MODEL_PATH)
    model = model_data['model']
    scaler = model_data['scaler']
    features = model_data['features']
    print(f"Loaded successfully. Model type: {type(model).__name__}. Features: {features}")
else:
    raise FileNotFoundError(f"Saved model package '{MODEL_PATH}' not found. Please run train_models.py first.")

@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/predict_input')
def predict_input():
    defaults = {
        'Annual_Rainfall': 2200,
        'Seasonal_Rainfall': 1600,
        'Cloud_Visibility': 6.0,
        'Temperature': 28.0,
        'Humidity': 75,
        'Wind_Speed': 18.0,
        'Pressure': 1009.0,
        'Weather_Condition': 'Cloudy'
    }
    return render_template('predict_input.html', defaults=defaults)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        annual_rainfall = float(request.form.get('Annual_Rainfall'))
        seasonal_rainfall = float(request.form.get('Seasonal_Rainfall'))
        cloud_visibility = float(request.form.get('Cloud_Visibility'))
        temperature = float(request.form.get('Temperature'))
        humidity = float(request.form.get('Humidity'))
        wind_speed = float(request.form.get('Wind_Speed'))
        pressure = float(request.form.get('Pressure'))
        weather_condition = request.form.get('Weather_Condition')
        
        weather_cloudy = 1 if weather_condition == 'Cloudy' else 0
        weather_overcast = 1 if weather_condition == 'Overcast' else 0
        weather_rainy = 1 if weather_condition == 'Rainy' else 0
        weather_sunny = 1 if weather_condition == 'Sunny' else 0
        
        input_data = pd.DataFrame([{
            'Annual_Rainfall': annual_rainfall,
            'Seasonal_Rainfall': seasonal_rainfall,
            'Cloud_Visibility': cloud_visibility,
            'Temperature': temperature,
            'Humidity': humidity,
            'Wind_Speed': wind_speed,
            'Pressure': pressure,
            'Weather_Cloudy': weather_cloudy,
            'Weather_Overcast': weather_overcast,
            'Weather_Rainy': weather_rainy,
            'Weather_Sunny': weather_sunny
        }])
        
        input_data = input_data[features]
        input_scaled = scaler.transform(input_data)
        
        prediction = int(model.predict(input_scaled)[0])
        probabilities = model.predict_proba(input_scaled)[0]
        flood_prob = float(probabilities[1]) * 100
        
        session['inputs'] = {
            'Annual_Rainfall': annual_rainfall,
            'Seasonal_Rainfall': seasonal_rainfall,
            'Cloud_Visibility': cloud_visibility,
            'Temperature': temperature,
            'Humidity': humidity,
            'Wind_Speed': wind_speed,
            'Pressure': pressure,
            'Weather_Condition': weather_condition
        }
        session['prediction'] = prediction
        session['flood_probability'] = round(flood_prob, 2)
        
        if prediction == 1:
            return redirect(url_for('result_flood'))
        else:
            return redirect(url_for('result_no_flood'))
            
    except Exception as e:
        print(f"Error during prediction: {e}")
        defaults = {
            'Annual_Rainfall': request.form.get('Annual_Rainfall', 2200),
            'Seasonal_Rainfall': request.form.get('Seasonal_Rainfall', 1600),
            'Cloud_Visibility': request.form.get('Cloud_Visibility', 6.0),
            'Temperature': request.form.get('Temperature', 28.0),
            'Humidity': request.form.get('Humidity', 75),
            'Wind_Speed': request.form.get('Wind_Speed', 18.0),
            'Pressure': request.form.get('Pressure', 1009.0),
            'Weather_Condition': request.form.get('Weather_Condition', 'Cloudy')
        }
        return render_template('predict_input.html', defaults=defaults, error=f"Invalid inputs: {str(e)}")

@app.route('/result_flood')
def result_flood():
    if 'prediction' not in session or 'inputs' not in session:
        return redirect(url_for('index'))
    
    return render_template('result_flood.html', 
                           probability=session.get('flood_probability'),
                           inputs=session.get('inputs'))

@app.route('/result_no_flood')
def result_no_flood():
    if 'prediction' not in session or 'inputs' not in session:
        return redirect(url_for('index'))
        
    return render_template('result_no_flood.html', 
                           probability=session.get('flood_probability'),
                           inputs=session.get('inputs'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
