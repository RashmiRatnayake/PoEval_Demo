import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC


FEATURE_NAMES = [
    "temperature",
    "humidity",
    "pressure",
    "vibration",
    "battery",
    "latency",
]


def shannon_entropy(prob: float) -> float:
    prob = np.clip(prob, 1e-12, 1 - 1e-12)
    return float(-(prob * np.log2(prob) + (1 - prob) * np.log2(1 - prob)))


def generate_training_data(n_samples: int = 3000, seed: int = 42):
    rng = np.random.default_rng(seed)

    normal_temp = rng.normal(24, 2.5, n_samples)
    normal_humidity = rng.normal(55, 8, n_samples)
    normal_pressure = rng.normal(101.3, 1.0, n_samples)
    normal_vibration = rng.normal(0.4, 0.15, n_samples)
    normal_battery = rng.normal(78, 12, n_samples)
    normal_latency = rng.normal(40, 10, n_samples)

    X_normal = np.column_stack([
        normal_temp,
        normal_humidity,
        normal_pressure,
        normal_vibration,
        normal_battery,
        normal_latency,
    ])
    y_normal = np.ones(n_samples, dtype=int)  # trustworthy

    anom_temp = rng.choice([rng.normal(-10, 5, n_samples), rng.normal(85, 8, n_samples)]).reshape(-1)
    anom_humidity = rng.choice([rng.normal(0, 5, n_samples), rng.normal(100, 5, n_samples)]).reshape(-1)
    anom_pressure = rng.normal(110, 4, n_samples)
    anom_vibration = rng.normal(3.5, 1.0, n_samples)
    anom_battery = rng.normal(8, 5, n_samples)
    anom_latency = rng.normal(250, 80, n_samples)

    X_anom = np.column_stack([
        anom_temp,
        anom_humidity,
        anom_pressure,
        anom_vibration,
        anom_battery,
        anom_latency,
    ])
    y_anom = np.zeros(n_samples, dtype=int)  # untrustworthy

    X = np.vstack([X_normal, X_anom])
    y = np.concatenate([y_normal, y_anom])

    return X, y


def build_model(model_type: str):
    X, y = generate_training_data()

    if model_type == "rf":
        model = RandomForestClassifier(n_estimators=120, random_state=42)
    elif model_type == "mlp":
        model = MLPClassifier(hidden_layer_sizes=(32,), max_iter=500, random_state=42)
    elif model_type == "svm":
        model = SVC(probability=True, kernel="rbf", random_state=42)
    else:
        raise ValueError(f"Unsupported model type: {model_type}")

    model.fit(X, y)
    return model


def record_to_vector(record: dict):
    return np.array([[
        float(record["temperature"]),
        float(record["humidity"]),
        float(record["pressure"]),
        float(record["vibration"]),
        float(record["battery"]),
        float(record["latency"]),
    ]])