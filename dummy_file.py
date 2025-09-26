import pickle
import os
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Create directories if they don't exist
os.makedirs('data/models', exist_ok=True)

# Create dummy models for each risk type
for risk_type in ['bank', 'insurance', 'fintech']:
    # Create a dummy Random Forest model
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    
    # Train on dummy data
    X_dummy = np.random.randn(100, 10)
    y_dummy = np.random.randint(0, 2, 100)
    model.fit(X_dummy, y_dummy)
    
    # Save the model
    with open(f'data/models/{risk_type}_model.pkl', 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Created dummy model for {risk_type}")

print("Dummy models created successfully!")