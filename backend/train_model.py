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
        score = 10 + (row['speed'] * 0.4) + (row['curvature'] * 30)
        if row['roadType'] == 'Highway': score -= 10
        if row['roadType'] == 'Urban': score += 5
        if row['roadType'] == 'Rural': score += 10
        if row['weather'] != 'Clear': score += 15
        if row['lighting'] == 'Night': score += 20
        score += np.random.normal(0, 5)
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
