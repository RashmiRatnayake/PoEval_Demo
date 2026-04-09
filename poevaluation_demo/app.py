from flask import Flask, render_template, jsonify, request
import requests
from data_generator import generate_record

app = Flask(__name__)

COORDINATOR_SUBMIT_URL = "http://127.0.0.1:5000/submit"
COORDINATOR_STATUS_URL = "http://127.0.0.1:5000/status"
BLOCKCHAIN_CHAIN_URL = "http://127.0.0.1:6001/chain"
BLOCKCHAIN_PENDING_URL = "http://127.0.0.1:6001/pending"


@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/generate", methods=["POST"])
def generate():
    payload = request.get_json() or {}
    anomalous_probability = float(payload.get("anomalous_probability", 0.25))
    record = generate_record(anomalous_probability=anomalous_probability)
    response = requests.post(COORDINATOR_SUBMIT_URL, json={"record": record}, timeout=10)
    return jsonify(response.json())


@app.route("/state", methods=["GET"])
def state():
    coordinator = requests.get(COORDINATOR_STATUS_URL, timeout=10).json()
    chain = requests.get(BLOCKCHAIN_CHAIN_URL, timeout=10).json()
    pending = requests.get(BLOCKCHAIN_PENDING_URL, timeout=10).json()

    return jsonify({
        "coordinator": coordinator,
        "chain": chain,
        "pending": pending,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7000, debug=True)