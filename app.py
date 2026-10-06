"""PhishGuard Flask web application."""

from pathlib import Path

import joblib
from flask import Flask, render_template, request

from src.feature_extraction import extract_features

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "phishguard_model.joblib"

model_data = joblib.load(MODEL_PATH)
model = model_data["model"]
feature_names = model_data["features"]


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    confidence = None
    url = ""
    features = None

    if request.method == "POST":
        url = request.form.get("url", "").strip()

        if not url:
            result = "Please enter a URL."
        else:
            extracted = extract_features(url)
            feature_values = [[extracted[name] for name in feature_names]]

            prediction = model.predict(feature_values)[0]
            probabilities = model.predict_proba(feature_values)[0]

            if prediction == 1:
                result = "Potential Phishing URL"
                confidence = round(probabilities[1] * 100, 2)
            else:
                result = "Legitimate URL"
                confidence = round(probabilities[0] * 100, 2)

            features = extracted

    return render_template(
        "index.html",
        result=result,
        confidence=confidence,
        url=url,
        features=features,
    )


if __name__ == "__main__":
    app.run(debug=True)
