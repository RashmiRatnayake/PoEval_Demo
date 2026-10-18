from flask import Flask, request, jsonify
import requests
from collections import Counter

app = Flask(__name__)

EVALUATOR_URLS = [
    "http://127.0.0.1:5001/evaluate",
    "http://127.0.0.1:5002/evaluate",
    "http://127.0.0.1:5003/evaluate",
]

BLOCKCHAIN_APPEND_URL = "http://127.0.0.1:6001/append"

audit_log = []
accepted_count = 0
rejected_count = 0


@app.route("/submit", methods=["POST"])
def submit_record():
    global accepted_count, rejected_count

    payload = request.get_json()
    record = payload["record"]

    evaluator_results = []
    for url in EVALUATOR_URLS:
        response = requests.post(url, json={"record": record}, timeout=10)
        evaluator_results.append(response.json())

    labels = [res["label"] for res in evaluator_results]
    vote_counter = Counter(labels)

    final_label = "trustworthy" if vote_counter["trustworthy"] >= 2 else "untrustworthy"
    avg_score = round(sum(r["trust_score"] for r in evaluator_results) / len(evaluator_results), 4)
    avg_conf = round(sum(r["confidence"] for r in evaluator_results) / len(evaluator_results), 4)

    blockchain_response = None
    if final_label == "trustworthy":
        accepted_count += 1
        blockchain_response = requests.post(
            BLOCKCHAIN_APPEND_URL,
            json={"record": {
                "record_id": record["record_id"],
                "provider": record["provider"],
                "timestamp": record["timestamp"],
                "data": record,
                "avg_trust_score": avg_score,
                "avg_confidence": avg_conf,
                "decision": final_label,
            }},
            timeout=10
        ).json()
    else:
        rejected_count += 1

    result = {
        "record": record,
        "evaluator_results": evaluator_results,
        "final_label": final_label,
        "avg_trust_score": avg_score,
        "avg_confidence": avg_conf,
        "blockchain_result": blockchain_response,
    }

    audit_log.insert(0, result)

    return jsonify(result)


@app.route("/status", methods=["GET"])
def status():
    return jsonify({
        "accepted_count": accepted_count,
        "rejected_count": rejected_count,
        "recent_results": audit_log,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)