from flask import Flask, request, jsonify
from models import build_model, record_to_vector, shannon_entropy
import sys

app = Flask(__name__)

MODEL_TYPE = sys.argv[1] if len(sys.argv) > 1 else "rf"
NODE_ID = sys.argv[2] if len(sys.argv) > 2 else "eval-1"

model = build_model(MODEL_TYPE)


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "node_id": NODE_ID, "model_type": MODEL_TYPE})


@app.route("/evaluate", methods=["POST"])
def evaluate():
    payload = request.get_json()
    record = payload["record"]

    X = record_to_vector(record)
    prob_trust = float(model.predict_proba(X)[0][1])
    entropy = shannon_entropy(prob_trust)
    confidence = 1.0 - entropy
    label = "trustworthy" if prob_trust >= 0.5 else "untrustworthy"

    return jsonify({
        "node_id": NODE_ID,
        "model_type": MODEL_TYPE,
        "record_id": record["record_id"],
        "trust_score": round(prob_trust, 4),
        "uncertainty": round(entropy, 4),
        "confidence": round(confidence, 4),
        "label": label,
    })


if __name__ == "__main__":
    port = int(sys.argv[3]) if len(sys.argv) > 3 else 5001
    app.run(host="0.0.0.0", port=port, debug=False)