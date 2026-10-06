"""PhishGuard Flask application entry point."""

from flask import Flask

app = Flask(__name__)


@app.get("/")
def home():
    return "PhishGuard is ready. Model integration coming next."


if __name__ == "__main__":
    app.run(debug=True)
