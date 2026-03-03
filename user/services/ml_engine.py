import joblib
import numpy as np
import os

# Get project base directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "ml", "resistance_model.pkl")

# Load model once
model = joblib.load(MODEL_PATH)


def ml_predict(age, gender, bacteria_id, antibiotic_id):
    """
    Returns probability of resistance (0 to 1)
    """

    # Convert gender to numeric
    gender_val = 1 if gender.lower() == "male" else 0

    input_data = np.array([[age, gender_val, bacteria_id, antibiotic_id]])

    probability = model.predict_proba(input_data)[0][1]

    return float(probability)