"""Train the PhishGuard model using URL-only features.

The model receives only the URL itself. This keeps training consistent with
the final Flask application and avoids using webpage-derived features that
would not be available at prediction time.
"""

from pathlib import Path
import sys

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split

sys.path.insert(0, str(Path(__file__).resolve().parent))
from feature_extraction import extract_features

DATA_PATH = Path("data/PhiUSIIL_Phishing_URL_Dataset.csv")
MODEL_PATH = Path("models/phishguard_model.joblib")


def build_feature_table(urls: pd.Series) -> pd.DataFrame:
    return pd.DataFrame([extract_features(url) for url in urls])


def main() -> None:
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found at {DATA_PATH}. "
            "Run python src/download_dataset.py first."
        )

    df = pd.read_csv(DATA_PATH)

    if "URL" not in df.columns or "label" not in df.columns:
        raise ValueError(
            f"Expected columns 'URL' and 'label'. Found: {list(df.columns)}"
        )

    df = df.dropna(subset=["URL", "label"]).copy()

    X = build_feature_table(df["URL"])
    # UCI: label 1 = legitimate, label 0 = phishing.
    # PhishGuard: 0 = legitimate, 1 = phishing.
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

    accuracy = accuracy_score(y_test, predictions)
    print(f"Accuracy: {accuracy:.4f}")
    print("\nClassification report:")
    print(
        classification_report(
            y_test,
            predictions,
            target_names=["Legitimate", "Phishing"],
        )
    )
    print("Confusion matrix:")
    print(confusion_matrix(y_test, predictions))

    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(
        {
            "model": model,
            "features": list(X.columns),
            "target_mapping": {"0": "Legitimate", "1": "Phishing"},
        },
        MODEL_PATH,
    )
    print(f"\nSaved model to {MODEL_PATH}")


if __name__ == "__main__":
    main()
