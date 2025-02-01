# AgroPredict 🌾

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Flask](https://img.shields.io/badge/Framework-Flask-green)](https://flask.palletsprojects.com/)

A machine learning backend system for agricultural recommendations, providing:

1. 🌱 Optimal crop prediction based on soil parameters
2. 💊 Fertilizer recommendation based on nutrient analysis

## Features ✨
- 📈 Crop recommendation based on 7 environmental parameters
- 🌾 Fertilizer suggestion based on soil nutrient levels
- 🧠 Machine learning models for accurate predictions
- 🔄 REST API endpoints for easy integration
- 📦 Modular and scalable architecture

## Installation 💻

### Prerequisites
- Python 3.9+
- pip package manager

### Setup
```bash
git clone https://github.com/SakshamGarg16/AgroPredict-Backend.git
cd AgroPredict-Backend
pip install -r requirements.txt
```


### API Endpoints 🚀
1. Crop Prediction
Endpoint: POST /crop_prediction
Parameters:

```json
{
  "N": 90,         // Nitrogen level
  "P": 42,         // Phosphorous level
  "K": 43,         // Potassium level
  "temp": 20.5,    // Temperature
  "humid": 82,     // Humidity
  "ph": 6.5,       // Ph of soil
  "rain": 202      // rainfall
}
```

Response:
```json
{
  "recommended_crop": "maize",
}
```
2. Fertilizer Prediction
Endpoint: POST /fertilizer_prediction
Parameters:

```json
{
  "temp": 26,                  // Temperature
  "humid": 52,                 // Humidity
  "moist": 60,                 // Moisture
  "soil_type": "Sandy",       
  "crop_type": "Maize",
  "N": 42,                     // Nitrogen level
  "P": 50,                     // Phosphorous level
  "K": 40                      // Potassium level
}
```

Response:
```json
{
  "recommended_fertilizer": "Urea",
}
```
Project Structure 📁
```
AgroPredict-Backend/
├── Model/
│   ├── cropPred.pkl          # Crop recommendation model
│   └── fertilizerPred.pkl  # Fertilizer recommendation model
├── server.py                # Flask application entry point
├── util.py                  # Prediction logic
├── requirements.txt         # Dependency list
└── config.py                # Configuration settings
```

Usage Example 💡
``` python
import requests

# Crop prediction
response = requests.post('https://agropredict-backend-jf2h.onrender.com/crop_prediction', json={
    "N": 90,
    "P": 42,
    "K": 43,
    "temperature": 20.5,
    "humidity": 82,
    "ph": 6.5,
    "rainfall": 202
})
print(response.json())
```

Contributing 🤝
Fork the repository

Create feature branch: ``` git checkout -b feature/new-feature ```

Commit changes: ``` git commit -m 'Add new feature' ```

Push to branch: ``` git push origin feature/new-feature ```

Open a Pull Request
