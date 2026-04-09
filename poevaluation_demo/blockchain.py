from flask import Flask, request, jsonify
import hashlib
import json
from time import time

app = Flask(__name__)

blockchain = []
pending_records = []


def calculate_hash(block):
    block_string = json.dumps(block, sort_keys=True).encode()
    return hashlib.sha256(block_string).hexdigest()


def create_genesis_block():
    block = {
        "index": 0,
        "timestamp": time(),
        "records": [],
        "previous_hash": "0",
    }
    block["hash"] = calculate_hash(block)
    blockchain.append(block)


def create_block(records):
    previous_block = blockchain[-1]
    block = {
        "index": len(blockchain),
        "timestamp": time(),
        "records": records,
        "previous_hash": previous_block["hash"],
    }
    block["hash"] = calculate_hash(block)
    blockchain.append(block)
    return block


@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify(blockchain)


@app.route("/append", methods=["POST"])
def append_record():
    payload = request.get_json()
    accepted_record = payload["record"]
    pending_records.append(accepted_record)

    if len(pending_records) >= 5:
        block = create_block(pending_records.copy())
        pending_records.clear()
        return jsonify({"status": "block_created", "block": block})

    return jsonify({"status": "record_buffered", "buffer_size": len(pending_records)})


@app.route("/pending", methods=["GET"])
def get_pending():
    return jsonify(pending_records)


if __name__ == "__main__":
    create_genesis_block()
    app.run(host="0.0.0.0", port=6001, debug=False)