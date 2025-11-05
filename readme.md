## 🚗 Car Price Prediction Web App       

A simple machine learning web application built with Plotly Dash that predicts the resale price of a used car based on its specifications such as brand, year, mileage, engine size, and other features.       

This project demonstrates how to integrate a trained ML model into an interactive web interface, allowing users to enter car details and instantly get a predicted price.          

## How to use?

1. Clone the repository    

git clone https://github.com/yourusername/car-price-prediction.git     

2. python app.py

3. Navigate to 👉 http://127.0.0.1:8050 

## 🧮 Model Information

Trained Model: CPModel.pkl     
The model was trained using features such as:    

year     

km_driven     

mileage     

engine    

seats    

Brand (one-hot encoded)    

Seller type, transmission, and ownership details    

Scaler: scaler.gz    
Used to normalize numeric features before feeding them into the model.      