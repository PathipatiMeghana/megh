import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
import joblib

print("Loading dataset...")

df = pd.read_csv("clinical_amr_dataset.csv")

required_columns = ["age", "gender", "bacteria", "antibiotic", "result"]

for col in required_columns:
    if col not in df.columns:
        raise Exception(f"Column '{col}' not found in dataset!")

# Encode gender
df["gender"] = df["gender"].map({"Male": 1, "Female": 0})

# Encode bacteria & antibiotic
le_bacteria = LabelEncoder()
le_antibiotic = LabelEncoder()

df["bacteria_id"] = le_bacteria.fit_transform(df["bacteria"])
df["antibiotic_id"] = le_antibiotic.fit_transform(df["antibiotic"])

# Convert result to binary (R=1, S/I=0)
df["resistant"] = df["result"].map({
    "R": 1,
    "S": 0,
    "I": 0
})

X = df[["age", "gender", "bacteria_id", "antibiotic_id"]]
y = df["resistant"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))

print("Clinical Model Accuracy:", round(accuracy, 3))

joblib.dump(model, "clinical_model.pkl")
joblib.dump(le_bacteria, "clinical_bacteria_encoder.pkl")
joblib.dump(le_antibiotic, "clinical_antibiotic_encoder.pkl")

print("Clinical model saved successfully!")