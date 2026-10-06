"""Train a baseline PhishGuard model on the UCI PhiUSIIL dataset.

Download the dataset through ucimlrepo before running this script.
The UCI dataset uses label=1 for legitimate URLs and label=0 for phishing.
This script converts that convention to a model target where 1=phishing.
"""

from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

DATA_PATH = Path("data/PhiUSIIL_Phishing_URL_Dataset.csv")
MODEL_PATH = Path("models/phishguard_model.joblib")

# Numeric URL/page features supplied by the dataset.
FEATURE_COLUMNS = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "URLSimilarityIndex",
    "CharContinuationRate",
    "TLDLegitimateProb",
    "URLCharProb",
    "NoOfSubDomain",
    "HasObfuscation",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "NoOfLettersInURL",
    "NoOfDegitsInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "IsHTTPS",
]


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Download it from the UCI PhiUSIIL dataset page first."
        )

    df = pd.read_csv(DATA_PATH)

    missing = [c for c in FEATURE_COLUMNS + ["label"] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    df = df.dropna(subset=FEATURE_COLUMNS + ["label"]).copy()

    X = df[FEATURE_COLUMNS]
    # UCI: 1=legitimate, 0=phishing. Convert to 1=phishing for this project.
    y = (df["label"] == 0).astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
    print("\nClassification report:")
    print(classification_report(y_test, predictions, target_names=["Legitimate", "Phishing"]))
    print("Confusion matrix:")
    print(confusion_matrix(y_test, predictions))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {"model": model, "features": FEATURE_COLUMNS},
        MODEL_PATH,
    )
    print(f"\nSaved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
