
import csv
from datetime import date
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATASET_PATH = PROJECT_ROOT / "data" / "daily-rainfall-at-state-level.csv"


def predict_rainfall(state_code: int, forecast_date: str):
    """Estimate rainfall for a state and date using historical data."""

    if not 1 <= state_code:
        raise ValueError("State code must be a positive integer.")

    try:
        year, month, day = map(int, forecast_date.split("-"))
        date(year, month, day)
    except (ValueError, TypeError):
        raise ValueError("Date must be valid and use YYYY-MM-DD format.")

    records = []

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                code = int(row["state_code"])
                actual = float(row["actual"])
                normal = float(row["normal"]) if row["normal"] else np.nan

                if code == state_code and np.isfinite(actual):
                    records.append((row["date"], actual, normal))

            except (ValueError, TypeError):
                continue

    if not records:
        raise ValueError(
            f"No historical rainfall records found for state code {state_code}."
        )

    # Use the same general feature structure as the existing model.
    all_state_codes = set()

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                all_state_codes.add(int(row["state_code"]))
            except (ValueError, TypeError):
                continue

    state_codes = sorted(all_state_codes)
    state_index = {code: i for i, code in enumerate(state_codes)}

    valid_normals = [r[2] for r in records if np.isfinite(r[2])]
    if not valid_normals:
        raise ValueError("No normal rainfall values available for this state.")

    normal_median = float(np.median(valid_normals))

    X = []
    y = []

    for record_date, actual, normal in records:
        try:
            record_year, record_month, record_day = map(
                int, record_date.split("-")
            )
        except ValueError:
            continue

        if not np.isfinite(normal):
            normal = normal_median

        state_features = [0.0] * len(state_codes)
        state_features[state_index[state_code]] = 1.0

        features = state_features + [
            record_year - 2009,
            np.sin(2 * np.pi * record_month / 12),
            np.cos(2 * np.pi * record_month / 12),
            record_day,
            normal,
        ]

        X.append(features)
        y.append(actual)

    if not X:
        raise ValueError("Could not prepare historical training data.")

    X = np.asarray(X, dtype=float)
    y = np.asarray(y, dtype=float)

    X_bias = np.column_stack([np.ones(len(X)), X])
    weights = np.linalg.lstsq(X_bias, y, rcond=None)[0]

    # Estimate the normal value from this state's historical data.
    forecast_normals = [
        normal for _, _, normal in records if np.isfinite(normal)
    ]
    normal_for_forecast = float(np.median(forecast_normals))

    forecast_state = [0.0] * len(state_codes)
    forecast_state[state_index[state_code]] = 1.0

    forecast_features = forecast_state + [
        year - 2009,
        np.sin(2 * np.pi * month / 12),
        np.cos(2 * np.pi * month / 12),
        day,
        normal_for_forecast,
    ]

    forecast_row = np.array([1.0] + forecast_features, dtype=float)
    estimate = float(forecast_row @ weights)

    return {
        "state_code": state_code,
        "forecast_date": forecast_date,
        "estimated_rainfall_mm": round(max(estimate, 0.0), 2),
        "note": (
            "Experimental historical-data estimate, not a weather-service "
            "forecast. Validate the model before relying on it."
        ),
    }
