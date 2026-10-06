"""Download the UCI PhiUSIIL phishing URL dataset.

Run:
    python src/download_dataset.py

The official UCI download is a ZIP archive. The extracted CSV is saved under
data/ and is ignored by Git.
"""

from pathlib import Path
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO

DATA_DIR = Path("data")
OUTPUT = DATA_DIR / "PhiUSIIL_Phishing_URL_Dataset.csv"
DOWNLOAD_URL = "https://archive.ics.uci.edu/static/public/967/phiusiil%2Bphishing%2Burl%2Bdataset.zip"


def main() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    print("Downloading PhiUSIIL dataset from the official UCI repository...")
    with urlopen(DOWNLOAD_URL, timeout=120) as response:
        archive = BytesIO(response.read())

    print("Extracting dataset...")
    with ZipFile(archive) as zip_file:
        csv_files = [name for name in zip_file.namelist() if name.lower().endswith(".csv")]
        if not csv_files:
            raise RuntimeError("No CSV file found inside the UCI dataset archive.")

        source_name = csv_files[0]
        with zip_file.open(source_name) as source, OUTPUT.open("wb") as target:
            target.write(source.read())

    print(f"Saved dataset to: {OUTPUT}")
    print("You can now run: python src/train_model.py")


if __name__ == "__main__":
    main()
