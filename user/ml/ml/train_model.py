import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

print("Loading dataset...")

# =========================
# Load dataset
# =========================
df = pd.read_csv("clinical_amr_dataset.csv")

# Convert column names to lowercase
df.columns = df.columns.str.lower()

print("Available columns:", df.columns.tolist())
print("Total rows before cleaning:", len(df))

# =========================
# Rename columns if needed
# (Adjust automatically if dataset uses different names)
# =========================
rename_map = {}

if "bacteria_name" in df.columns:
    rename_map["bacteria_name"] = "bacteria"

if "antibiotic_name" in df.columns:
    rename_map["antibiotic_name"] = "antibiotic"

if "sex" in df.columns:
    rename_map["sex"] = "gender"

if "age_years" in df.columns:
    rename_map["age_years"] = "age"

df = df.rename(columns=rename_map)

# =========================
# Check required columns
# =========================
required_columns = ["age", "gender", "bacteria", "antibiotic", "result"]

for col in required_columns:
    if col not in df.columns:
        raise Exception(f"Column '{col}' not found in dataset!")

# =========================
# Remove missing rows
# =========================
df = df.dropna(subset=required_columns)

print("Total rows after cleaning:", len(df))

# =========================
# Encode gender
# =========================
df["gender"] = df["gender"].astype(str).str.lower()
df["gender"] = df["gender"].map({
    "male": 1,
    "female": 0
})

# =========================
# Convert result to binary
# =========================
df["result"] = df["result"].astype(str).str.upper()

# Keep only S, I, R
df = df[df["result"].isin(["S", "I", "R"])]

# Encode result (3 classes)
result_encoder = LabelEncoder()
df["result_encoded"] = result_encoder.fit_transform(df["result"])
# =========================
# Encode bacteria
# =========================
bacteria_encoder = LabelEncoder()
df["bacteria_id"] = bacteria_encoder.fit_transform(df["bacteria"])

# =========================
# Encode antibiotic
# =========================
antibiotic_encoder = LabelEncoder()
df["antibiotic_id"] = antibiotic_encoder.fit_transform(df["antibiotic"])

# =========================
# Features & Target
# =========================
X = df[["age", "gender", "bacteria_id", "antibiotic_id"]]
y = df["result_encoded"]

# =========================
# Train/Test Split
# =========================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# =========================
# Train Model
# =========================
model = RandomForestClassifier(
    n_estimators=200,
    class_weight="balanced",
    random_state=42
)

# =========================
# Evaluate
# =========================
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"Model Accuracy: {accuracy * 100:.2f}%")

# =========================
# Save Model & Encoders
# =========================
joblib.dump(model, "resistance_model.pkl")
joblib.dump(bacteria_encoder, "bacteria_encoder.pkl")
joblib.dump(antibiotic_encoder, "antibiotic_encoder.pkl")
joblib.dump(result_encoder, "result_encoder.pkl")
print("Model trained & saved successfully!")