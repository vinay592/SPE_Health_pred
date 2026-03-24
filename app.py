from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)

model = joblib.load("model/health_model.pkl")
scaler = joblib.load("model/scaler.pkl")

def validate_input(age, bp, chol, thalach, oldpeak, cp, exang):
    if not (20 <= age <= 80):
        return "Age must be between 20 and 80"
    if not (90 <= bp <= 180):
        return "Blood Pressure must be between 90 and 180"
    if not (150 <= chol <= 350):
        return "Cholesterol must be between 150 and 350"
    if not (70 <= thalach <= 200):
        return "Heart rate must be between 70 and 200"
    if not (0 <= oldpeak <= 6):
        return "Oldpeak must be between 0 and 6"
    if cp not in [0, 1, 2, 3]:
        return "CP must be 0,1,2,3"
    if exang not in [0, 1]:
        return "Exang must be 0 or 1"
    return None

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input received"})

    try:
        age = float(data.get('age', 0))
        bp = float(data.get('bp', 0))
        chol = float(data.get('chol', 0))
        thalach = float(data.get('thalach', 0))
        oldpeak = float(data.get('oldpeak', 0))
        cp = int(data.get('cp', 0))
        exang = int(data.get('exang', 0))
    except:
        return jsonify({"error": "Invalid input format"})

    logging.info(f"Received: {age}, {bp}, {chol}, {thalach}, {oldpeak}, {cp}, {exang}")

    error = validate_input(age, bp, chol, thalach, oldpeak, cp, exang)
    if error:
        return jsonify({"error": error})

    try:
        input_data = np.array([[age, bp, chol, thalach, oldpeak, cp, exang]], dtype=float)
        input_scaled = scaler.transform(input_data)
        prediction = model.predict(input_scaled)[0]
    except Exception as e:
        logging.error(f"Model error: {e}")
        return jsonify({"error": "Model prediction failed"})

    # 🔥 ML BASE DECISION (PRIMARY)
    risk = "High" if prediction == 1 else "Low"

    # 🔥 LIGHT ADJUSTMENTS (NOT DOMINATING)
    if risk == "Low":
        if chol >= 260 or bp >= 150 or oldpeak >= 3:
            risk = "Moderate"

    # 🔥 EXTREME SAFETY OVERRIDE (RARE ONLY)
    if chol >= 330 or bp >= 170 or oldpeak >= 5 or thalach > 185:
        risk = "High"

    # 🔥 REASONS (ONLY IF NOT LOW)
    reasons = []

    if risk != "Low":
        if bp >= 140:
            reasons.append("High Blood Pressure")

        if chol >= 240:
            reasons.append("High Cholesterol")

        if oldpeak >= 2:
            reasons.append("Cardiac Stress")

        if exang == 1:
            reasons.append("Exercise Induced Angina")

        if age >= 55:
            reasons.append("Age Risk")

        if thalach > 170:
            reasons.append("Elevated Heart Rate")

        if thalach < 90:
            reasons.append("Low Heart Rate")

    # 🔥 RECOMMENDATIONS
    recommendations = []

    if risk in ["Moderate", "High"]:

        if "High Blood Pressure" in reasons:
            recommendations.append("Reduce salt intake and monitor BP regularly")

        if "High Cholesterol" in reasons:
            recommendations.append("Avoid oily and fried foods")

        if "Cardiac Stress" in reasons:
            recommendations.append("Reduce stress and avoid heavy exertion")

        if "Exercise Induced Angina" in reasons:
            recommendations.append("Consult doctor before physical activity")

        if "Age Risk" in reasons:
            recommendations.append("Schedule regular health checkups")

        if "Elevated Heart Rate" in reasons:
            recommendations.append("Avoid intense physical activity and monitor heart rate")

    if risk == "Moderate":
        recommendations.append("Maintain a healthy lifestyle and monitor your health regularly")

    if risk == "High":
        recommendations.append("Consult a doctor immediately")

    # 🔥 CLEAN LOW OUTPUT
    if risk == "Low":
        reasons = []
        recommendations = ["Your health parameters are within normal range. Maintain a healthy lifestyle."]

    return jsonify({
        "risk": risk,
        "reasons": reasons,
        "recommendations": recommendations
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
