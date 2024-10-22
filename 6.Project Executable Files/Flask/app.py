# app.py
from flask import Flask, render_template, request
import pickle
import pandas as pd

def create_app():
    app = Flask(__name__)

    # Load the model
    model = pickle.load(open('RFmodel.pkl', 'rb'))
    scaler = pickle.load(open('scaler.pkl', 'rb'))


    @app.route('/')
    def home():
        return render_template('index.html')


    @app.route('/predict', methods=['POST'])
    def predict():
    # Get data from form in the specified order
        humidity_3pm = float(request.form['Humidity3pm'])
        rainfall = float(request.form['Rainfall'])
        cloud_3pm = float(request.form['Cloud3pm'])
        humidity_9am = float(request.form['Humidity9am'])
        cloud_9am = float(request.form['Cloud9am'])
        wind_gust_speed = float(request.form['WindGustSpeed'])
        wind_speed_9am = float(request.form['WindSpeed9am'])
        min_temp = float(request.form['MinTemp'])
        wind_speed_3pm = float(request.form['WindSpeed3pm'])
        wind_gust_dir = int(request.form['WindGustDir'])

        # Define feature names
        feature_names = ['Humidity3pm', 'Rainfall', 'Cloud3pm', 'Humidity9am', 'Cloud9am', 'WindGustSpeed', 'WindSpeed9am', 'MinTemp', 'WindSpeed3pm', 'WindGustDir']

        # Create the data array in the specified order
        data = [humidity_3pm, rainfall, cloud_3pm, humidity_9am, cloud_9am, wind_gust_speed, wind_speed_9am, min_temp, wind_speed_3pm, wind_gust_dir]

        # Create a DataFrame with the feature names
        input_data = pd.DataFrame([data], columns=feature_names)
        #print("Input Data:\n", input_data) 

        input_data_scaled = scaler.transform(input_data)
        #print("Scaled Input Data:\n", input_data_scaled) 
        input_data_scaled_df = pd.DataFrame(input_data_scaled, columns=feature_names)

        # Make prediction
        prediction = model.predict(input_data_scaled_df)
        #print("Prediction:", prediction)

        # Assuming the model returns 1 for rain and 0 for no rain
        if prediction[0] == 1:
            return render_template('rain.html')
        else:
            return render_template('norain.html')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
