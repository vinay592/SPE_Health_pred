import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Load dataset
data = pd.read_csv("/home/vinay-v-bhandare/Documents/SPE_Project/health-ml/data/dataset.csv")

# Select relevant features
data = data[['age', 'trestbps', 'chol', 'thalach', 'oldpeak', 'cp', 'exang', 'target']]

# Split features and target
X = data.drop('target', axis=1)
y = data['target']

# 🔥 Apply scaling
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Model
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=5,
    random_state=42
)

# Train
model.fit(X_train, y_train)

# Evaluate
accuracy = model.score(X_test, y_test)
print("Accuracy:", accuracy)

# Create model directory
os.makedirs("model", exist_ok=True)

# Save model + scaler
joblib.dump(model, "model/health_model.pkl")
joblib.dump(scaler, "model/scaler.pkl")

print("Model and scaler saved successfully")
