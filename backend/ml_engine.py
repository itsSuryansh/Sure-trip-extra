import joblib
import numpy as np
import os


MODEL_PATH = os.path.join("models", "suretrip_final_model.pkl")

model = joblib.load(MODEL_PATH)


FEATURE_ORDER = [
    "distance_km",
    "total_base_time_min",
    "total_buffer_min",
    "total_variance_min",
    "total_cost_inr",
    "n_legs",
    "has_flight",
    "has_train",
    "tightest_buffer_ratio",
    "max_leg_variance_min",
    "min_buffer_min",
    "variance_pct_of_base",
    "buffer_pct_of_base",
    "deadline_multiplier",
    "option_type_enc",
    "src_delhi",
    "src_lucknow",
    "src_chandigarh",
    "src_jaipur",
    "src_pune",
    "dst_delhi",
    "dst_lucknow",
    "dst_chandigarh",
    "dst_jaipur",
    "dst_pune",
    "std_arrival_min",
    "mean_final_delay_min",
    "risk_level_enc"
]


def predict_reliability(data: dict):

    features = []

    for col in FEATURE_ORDER:
        features.append(data[col])

    arr = np.array([features])

    pred = model.predict(arr)[0]

    return round(float(pred), 2)