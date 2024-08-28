import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from .config import config

# Define paths for model storage
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.pkl')
DATA_PATH = os.path.join(os.path.dirname(__file__), 'data.csv')

def load_data():
    """Load and return training data."""
    import pandas as pd
    data = pd.read_csv(DATA_PATH)
    return data

def train_model():
    """Train a machine learning model and save it to disk."""
    data = load_data()
    X = data.drop('target', axis=1)
    y = data['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    
    print("Model trained and saved to disk.")

def predict(input_data):
    """Load the trained model and make predictions."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model file does not exist.")
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    
    import numpy as np
    input_array = np.array(input_data).reshape(1, -1)
    prediction = model.predict(input_array)
    return prediction[0]

def get_metrics():
    """Return model performance metrics."""
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Model file does not exist.")
    
    data = load_data()
    X = data.drop('target', axis=1)
    y = data['target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    
    y_pred = model.predict(X_test)
    metrics = classification_report(y_test, y_pred, output_dict=True)
    return metrics
