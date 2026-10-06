# PhishGuard

PhishGuard is a machine-learning web application that analyzes website URLs and predicts whether they are potentially phishing or legitimate using explainable URL-based features.

## Features

- URL-based phishing classification
- Explainable feature extraction from the URL itself
- Random Forest machine-learning model
- Flask web interface
- Prediction score displayed in the UI
- URL feature summary after analysis
- Responsive interface for desktop and smaller screens

## How it works

1. The user enters a URL in the Flask web interface.
2. PhishGuard extracts URL-only characteristics such as:
   - URL and hostname length
   - Number of dots, hyphens and slashes
   - Query-string symbols
   - Digit count
   - HTTPS usage
   - IP-address usage
   - Subdomain count
   - Punycode
   - Suspicious keywords
3. The extracted features are passed to a trained Random Forest classifier.
4. The application displays either **Legitimate URL** or **Potential Phishing URL** with the model probability for the predicted class.

## Model evaluation

The model was evaluated on a stratified 20% held-out test split.

- **Test accuracy:** 99.57%
- **Test samples:** 47,159
- **Confusion matrix:**

```
[[26939,    31],
 [  173, 20016]]
```

The project uses URL-only features for both training and prediction so that the deployed application receives the same type of information used during model training.

> The reported accuracy is a held-out dataset result. It should not be interpreted as a guarantee of real-world phishing detection performance.

## Dataset

PhishGuard uses the **PhiUSIIL Phishing URL Dataset** from the UCI Machine Learning Repository.

- 235,795 URL records
- 54 original dataset features
- The project extracts a smaller set of URL-only features from the URL column for its final model
- UCI dataset: https://archive.ics.uci.edu/dataset/967/phiusil-phishing-url-dataset

The raw dataset is intentionally excluded from Git because of its size. Run the download script to obtain it locally.

## Tech stack

- Python
- Pandas
- NumPy
- Scikit-learn
- Flask
- Joblib
- Matplotlib

## Project structure

```
phishguard/
├── app.py
├── README.md
├── requirements.txt
├── data/
│   └── README.md
├── models/
│   └── phishguard_model.joblib   # generated locally, ignored by Git
├── src/
│   ├── download_dataset.py
│   ├── feature_extraction.py
│   └── train_model.py
├── templates/
│   └── index.html
└── static/
    └── style.css
```

## Setup and usage

### 1. Clone the repository

```bash
git clone https://github.com/sabaanjum-hue/phishguard.git
cd phishguard
```

### 2. Create and activate a virtual environment

Windows:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Download the dataset

```bash
python src/download_dataset.py
```

### 5. Train the model

```bash
python src/train_model.py
```

This creates:

```
models/phishguard_model.joblib
```

### 6. Start the Flask application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

## Screenshots

### Legitimate URL detection

![PhishGuard legitimate URL result](screenshots/legitimate-url.jpg)

### Potential phishing URL detection

![PhishGuard phishing URL result](screenshots/phishing-url.jpg)

## Example tests

Legitimate example:

```
https://www.google.com
```

Example URL with suspicious characteristics:

```
http://secure-login-example.com/verify/account
```

These examples are used only as text inputs to the local classifier. Do not visit suspicious URLs.

## Limitations

PhishGuard is an educational machine-learning project. It analyzes URL characteristics and does not inspect the live website, page content, certificates, reputation feeds, or browser behavior. A prediction is therefore not a definitive security verdict.

## Disclaimer

Use PhishGuard for educational and defensive purposes. Do not rely on the model alone when deciding whether a real-world URL is safe.
