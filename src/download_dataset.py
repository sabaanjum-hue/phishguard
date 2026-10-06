"""Download the UCI PhiUSIIL phishing URL dataset.

Run:
    python src/download_dataset.py

The raw CSV is saved under data/ and is ignored by Git.
"""

from pathlib import Path

from ucimlrepo import fetch_ucirepo


OUTPUT = Path("data/PhiUSIIL_Phishing_URL_Dataset.csv")


def main() -> None:
    print("Downloading UCI PhiUSIIL dataset...")
    dataset = fetch_ucirepo(id=967)

    features = dataset.data.features
    targets = dataset.data.targets

    # The UCI target column is expected to be named "label".
    if "label" not in targets.columns:
        raise ValueError(f"Expected target column 'label', found: {list(targets.columns)}")

    combined = features.copy()
    combined["label"] = targets["label"].values

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    combined.to_csv(OUTPUT, index=False)

    print(f"Saved {len(combined):,} rows to {OUTPUT}")


if __name__ == "__main__":
    main()
