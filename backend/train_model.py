import xgboost as xgb
import pandas as pd
import numpy as np

try:
    # 1. Generate Synthetic Data
    print("Generating synthetic training data...")
    n_samples = 1000
    data = {
        'speed': np.random.randint(30, 120, n_samples),
        'curvature': np.random.rand(n_samples),
        'roadType': np.random.choice(['Highway', 'Urban', 'Rural'], n_samples),
        'weather': np.random.choice(['Clear', 'Rain', 'Fog', 'Snow'], n_samples),
        'lighting': np.random.choice(['Day', 'Night', 'Dusk'], n_samples),
    }
    df = pd.DataFrame(data)

    def calculate_synthetic_risk(row):
        score = 5 # Base score
        
        # Speed: Core driver of risk (15-60 points)
        score += row['speed'] * 0.5 

        # Curvature: (0-40 points)
        score += row['curvature'] * 40 

        # Road Type Modifiers
        if row['roadType'] == 'Highway': score -= 5   # Safer infra
        if row['roadType'] == 'Urban': score += 10    # Pedestrians/Traffic
        if row['roadType'] == 'Rural': score += 5     # Unpredictable

        # Weather (Significant Impact)
        if row['weather'] == 'Snow': score += 40      # Very dangerous
        elif row['weather'] == 'Fog': score += 25
        elif row['weather'] == 'Rain': score += 15
        
        # Lighting
        if row['lighting'] == 'Night': score += 10
        elif row['lighting'] == 'Dusk': score += 5

        # Interactive Penalties (The "Killer" combos)
        # High speed in bad weather is deadly
        if row['speed'] > 70 and row['weather'] in ['Snow', 'Rain', 'Fog']: 
            score += 20
            
        # Curvy rural roads at night
        if row['roadType'] == 'Rural' and row['curvature'] > 0.5 and row['lighting'] == 'Night':
            score += 15

        score += np.random.normal(0, 3) # Reduced noise
        return min(99, max(1, score))

    df['risk'] = df.apply(calculate_synthetic_risk, axis=1)

    # 2. Preprocessing
    X = df.drop('risk', axis=1)
    y = df['risk']
    
    # Cast to int for native DMatrix compatibility
    X_encoded = pd.get_dummies(X, columns=['roadType', 'weather', 'lighting']).astype(int)
    feature_names = X_encoded.columns.tolist()

    print(f"Features: {feature_names}")

    # 3. Train using Native API
    print("Training XGBoost (Native API)...")
    
    dtrain = xgb.DMatrix(X_encoded, label=y, feature_names=feature_names)
    
    params = {
        'objective': 'reg:squarederror',
        'max_depth': 7,
        'eta': 0.05,
        'subsample': 0.8,
        'colsample_bytree': 0.8
    }
    
    model = xgb.train(params, dtrain, num_boost_round=100)

    # 4. Save Model
    print("Saving model to 'model.json'...")
    model.save_model("model.json") # Native JSON format

    import json
    with open("model_features.json", "w") as f:
        json.dump(feature_names, f)

    print("Done! You can now run the server.")

except Exception as e:
    import traceback
    with open("error.log", "w") as f:
        f.write(traceback.format_exc())
    print("Error occurred. Check error.log")
