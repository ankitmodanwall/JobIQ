import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

data = {
    "experience": [0, 1, 2, 3, 5, 7, 10],
    "salary": [3, 5, 7, 9, 12, 18, 25]
}

df = pd.DataFrame(data)

X = df[["experience"]]
y = df["salary"]

model = LinearRegression()
model.fit(X, y)

# joblib.dump(model, "app/ml/salary_model.pkl")
joblib.dump(model, "salary_model.pkl")
print("Model trained successfully!")