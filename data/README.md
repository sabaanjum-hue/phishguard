# Dataset

PhishGuard will use a labelled phishing-URL dataset with a URL column and a binary label column.

The raw dataset is intentionally not committed yet. Before training, we will verify the public dataset source, license, column names, and preprocessing steps.

Expected format:

- `url`: URL to analyse
- `label`: 0 for legitimate and 1 for phishing

Do not add passwords, API keys, private URLs, or other sensitive information.
