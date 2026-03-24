import pandas as pd
import random

# Load existing dataset
df = pd.read_csv("data/dataset.csv")

current_size = len(df)
target_size = 1000

rows = []

for _ in range(target_size - current_size):

    age = random.randint(20, 80)
    sex = random.randint(0, 1)
    cp = random.randint(0, 3)
    trestbps = random.randint(90, 180)
    chol = random.randint(150, 350)
    fbs = random.randint(0, 1)
    restecg = random.randint(0, 1)
    thalach = random.randint(70, 200)
    exang = random.randint(0, 1)
    oldpeak = round(random.uniform(0, 6), 1)
    slope = random.randint(0, 2)
    ca = random.randint(0, 3)
    thal = random.randint(1, 3)

    # SAME LOGIC → ensures consistency
    risk_score = 0

    if chol > 240:
        risk_score += 2
    if trestbps > 140:
        risk_score += 2
    if oldpeak > 2:
        risk_score += 2
    if exang == 1:
        risk_score += 1
    if age > 55:
        risk_score += 1

    target = 1 if risk_score >= 3 else 0

    rows.append([
        age, sex, cp, trestbps, chol, fbs,
        restecg, thalach, exang, oldpeak,
        slope, ca, thal, target
    ])

columns = df.columns
new_df = pd.DataFrame(rows, columns=columns)

# Append to original (no changes to existing data)
final_df = pd.concat([df, new_df], ignore_index=True)

# Save back
final_df.to_csv("data/dataset.csv", index=False)

print("Dataset extended to", len(final_df), "rows ✅")
