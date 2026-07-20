import unittest
from app import app

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        self.client = app.test_client()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Predicting Flood Risks', response.data)

    def test_predict_input_page(self):
        response = self.client.get('/predict_input')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flood Risk Predictor', response.data)

    def test_predict_low_risk(self):
        data = {
            'Annual_Rainfall': '1200.0',
            'Seasonal_Rainfall': '700.0',
            'Cloud_Visibility': '8.5',
            'Temperature': '32.0',
            'Humidity': '50.0',
            'Wind_Speed': '10.0',
            'Pressure': '1014.0',
            'Weather_Condition': 'Sunny'
        }
        response = self.client.post('/predict', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Minimal Flood Risk Detected', response.data)

    def test_predict_high_risk(self):
        data = {
            'Annual_Rainfall': '4200.0',
            'Seasonal_Rainfall': '3300.0',
            'Cloud_Visibility': '1.0',
            'Temperature': '22.0',
            'Humidity': '98.0',
            'Wind_Speed': '38.0',
            'Pressure': '990.0',
            'Weather_Condition': 'Rainy'
        }
        response = self.client.post('/predict', data=data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'High Flood Risk Detected', response.data)

if __name__ == '__main__':
    unittest.main()
