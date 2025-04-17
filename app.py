from flask import Flask, request, jsonify, render_template
import pickle
import pandas as pd
import numpy as np

app = Flask(__name__)

# Load the pickle file
with open('model/Lasso_prediction_pipeline.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.json
        
        # Create DataFrame with the same structure as training data
        input_df = pd.DataFrame({
            'Location': [data['Location']],
            'Area (sqft)': [data['Area']],
            'Bedrooms': [data['Bedrooms']],
            'Bathrooms': [data['Bathrooms']],
            'Parking Spaces': [data['ParkingSpaces']],
            'Age of Property (years)': [data['Age']],
            'Floor': [data['Floor']],
            'Total Floors': [data['TotalFloors']],
            'Furnishing': [data['Furnishing']],
            'Property Type': [data['PropertyType']],
            'Nearby Metro (Y/N)': [data['NearbyMetro']]
        })
        
        # Make prediction
        prediction = model.predict(input_df)
        
        # Return prediction
        return jsonify({
            'prediction': round(float(prediction[0]), 2),
            'unit': 'Lakhs'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)