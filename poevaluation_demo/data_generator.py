import random
import uuid
from datetime import datetime


def generate_record(anomalous_probability: float = 0.25):
    is_anomalous = random.random() < anomalous_probability

    if not is_anomalous:
        record = {
            "record_id": str(uuid.uuid4())[:8],
            "provider": random.choice(["Factory-A", "Factory-B", "Warehouse-C"]),
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": round(random.uniform(20, 28), 2),
            "humidity": round(random.uniform(45, 65), 2),
            "pressure": round(random.uniform(100.0, 102.5), 2),
            "vibration": round(random.uniform(0.2, 0.8), 2),
            "battery": round(random.uniform(55, 95), 2),
            "latency": round(random.uniform(20, 60), 2),
            "ground_truth": "normal",
        }
    else:
        record = {
            "record_id": str(uuid.uuid4())[:8],
            "provider": random.choice(["Factory-A", "Factory-B", "Warehouse-C"]),
            "timestamp": datetime.utcnow().isoformat(),
            "temperature": round(random.choice([random.uniform(-15, 0), random.uniform(75, 100)]), 2),
            "humidity": round(random.choice([random.uniform(0, 10), random.uniform(90, 100)]), 2),
            "pressure": round(random.uniform(106, 114), 2),
            "vibration": round(random.uniform(2.5, 6.0), 2),
            "battery": round(random.uniform(0, 20), 2),
            "latency": round(random.uniform(180, 400), 2),
            "ground_truth": "anomalous",
        }

    return record