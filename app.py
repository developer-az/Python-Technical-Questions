from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Python Technical Questions Practice Tool"


@app.route("/health")
def health():
    return {"status": "ok", "message": "Application is running"}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
