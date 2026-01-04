import xgboost as xgb
import pandas as pd
import json
import os

model = None
feature_names = None

def load_model():
    global model, feature_names
    
    model_path = os.path.join(os.path.dirname(__file__), "model.json")
    features_path = os.path.join(os.path.dirname(__file__), "model_features.json")
    
    if not os.path.exists(model_path):
        raise FileNotFoundError("Model file not found. Run 'python backend/train_model.py' first.")
        
    model = xgb.Booster()
    model.load_model(model_path)
    
    with open(features_path, "r") as f:
        feature_names = json.load(f)
        
    print("Model loaded successfully.")

def predict_risk(scenario):
    """
    scenario: dict { 'speed': 50, 'roadType': 'Highway', ... }
    """
    if model is None:
        load_model()
        
    df = pd.DataFrame([scenario])
    df_encoded = pd.get_dummies(df, columns=['roadType', 'weather', 'lighting']).astype(int)
    
    # Align features
    df_final = df_encoded.reindex(columns=feature_names, fill_value=0)
    
    # Native API prediction requires DMatrix
    dtest = xgb.DMatrix(df_final, feature_names=feature_names)
    
    prediction = model.predict(dtest)[0]
    
    return float(prediction)
