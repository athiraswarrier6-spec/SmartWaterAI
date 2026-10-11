import csv
import numpy as np


# ==========================================
# 1. LOAD DATASET
# ==========================================

file_path = "data/daily-rainfall-at-state-level.csv"

data = []

with open(file_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        try:
            actual = float(row["actual"]) if row["actual"] else np.nan
            normal = float(row["normal"]) if row["normal"] else np.nan
            state_code = int(row["state_code"])

            # Actual rainfall is our target.
            # Skip rows where actual rainfall is missing.
            if np.isnan(actual):
                continue

            data.append([
                state_code,
                row["date"],
                actual,
                normal
            ])

        except (ValueError, TypeError):
            continue


print("Valid records:", len(data))


# ==========================================
# 2. HANDLE MISSING NORMAL VALUES
# ==========================================

normal_values = [
    row[3] for row in data
    if not np.isnan(row[3])
]

normal_median = np.median(normal_values)

for row in data:
    if np.isnan(row[3]):
        row[3] = normal_median


# ==========================================
# 3. CREATE FEATURES
# ==========================================

state_codes = sorted(set(row[0] for row in data))
state_index = {state: i for i, state in enumerate(state_codes)}

X = []
y = []

for row in data:

    state_code = row[0]
    date = row[1]
    actual = row[2]
    normal = row[3]

    year, month, day = map(int, date.split("-"))

    # One-hot encoding for state
    state_features = [0] * len(state_codes)
    state_features[state_index[state_code]] = 1

    # Seasonal features
    month_sin = np.sin(2 * np.pi * month / 12)
    month_cos = np.cos(2 * np.pi * month / 12)

    # Final feature vector
    features = (
        state_features
        + [
            year - 2009,
            month_sin,
            month_cos,
            day,
            normal
        ]
    )

    X.append(features)
    y.append(actual)


X = np.array(X, dtype=float)
y = np.array(y, dtype=float)


print("Feature matrix:", X.shape)
print("Target values:", y.shape)


# ==========================================
# 4. TRAIN / TEST SPLIT
# ==========================================


# Sort records chronologically before splitting.
# The date is stored in each row as YYYY-MM-DD.
dates = np.array([row[1] for row in data])

chronological_indices = np.argsort(dates)

split = int(len(X) * 0.8)

train_indices = chronological_indices[:split]
test_indices = chronological_indices[split:]

X_train = X[train_indices]
X_test = X[test_indices]

y_train = y[train_indices]
y_test = y[test_indices]

print("Training date range:", dates[train_indices[0]],
      "to", dates[train_indices[-1]])
print("Testing date range:", dates[test_indices[0]],
      "to", dates[test_indices[-1]])



# ==========================================
# 5. ADD BIAS COLUMN
# ==========================================

X_train_bias = np.column_stack(
    [np.ones(len(X_train)), X_train]
)

X_test_bias = np.column_stack(
    [np.ones(len(X_test)), X_test]
)


# ==========================================
# 6. TRAIN LINEAR REGRESSION
# ==========================================

print("\nTraining ML model...")

# Least-squares solution
weights = np.linalg.lstsq(
    X_train_bias,
    y_train,
    rcond=None
)[0]

print("Training completed!")


# ==========================================
# 7. PREDICTIONS
# ==========================================

y_pred = X_test_bias @ weights
# Rainfall cannot be negative
y_pred = np.maximum(y_pred, 0)

# ==========================================
# 8. MODEL EVALUATION
# ==========================================

mae = np.mean(np.abs(y_test - y_pred))

mse = np.mean((y_test - y_pred) ** 2)

rmse = np.sqrt(mse)

ss_total = np.sum((y_test - np.mean(y_test)) ** 2)

ss_residual = np.sum((y_test - y_pred) ** 2)

r2 = 1 - (ss_residual / ss_total)

# ==========================================
# KERALA TEST PERFORMANCE
# ==========================================


# ==========================================
# KERALA TEST PERFORMANCE
# ==========================================

kerala_code = 32
kerala_index = state_index.get(kerala_code)

if kerala_index is not None:
    kerala_mask = X_test[:, kerala_index] == 1

    if np.any(kerala_mask):
        kerala_actual = y_test[kerala_mask]
        kerala_predicted = y_pred[kerala_mask]

        kerala_mae = np.mean(
            np.abs(kerala_actual - kerala_predicted)
        )

        kerala_rmse = np.sqrt(
            np.mean(
                (kerala_actual - kerala_predicted) ** 2
            )
        )

        # Kerala-specific baseline
        kerala_train_mask = X_train[:, kerala_index] == 1
        kerala_train_actual = y_train[kerala_train_mask]

        if len(kerala_train_actual) > 0:
            kerala_baseline = np.full(
                len(kerala_actual),
                np.mean(kerala_train_actual)
            )

            baseline_kerala_mae = np.mean(
                np.abs(kerala_actual - kerala_baseline)
            )

            baseline_kerala_rmse = np.sqrt(
                np.mean(
                    (kerala_actual - kerala_baseline) ** 2
                )
            )

            print("Kerala baseline MAE:", baseline_kerala_mae)
            print("Kerala baseline RMSE:", baseline_kerala_rmse)

        print("\nKERALA TEST RESULTS")
        print("-------------------")
        print("Test records:", len(kerala_actual))
        print("MAE :", kerala_mae)
        print("RMSE:", kerala_rmse)

    else:
        print("\nNo Kerala records found in the test set.")


# ==========================================
# BASELINE COMPARISON
# ==========================================

# Predict the average training rainfall for every test record.
baseline_prediction = np.full(
    len(y_test),
    np.mean(y_train)
)

baseline_mae = np.mean(
    np.abs(y_test - baseline_prediction)
)

baseline_rmse = np.sqrt(
    np.mean((y_test - baseline_prediction) ** 2)
)

baseline_r2 = 1 - (
    np.sum((y_test - baseline_prediction) ** 2) / ss_total
)

print("\nBASELINE MODEL RESULTS")
print("----------------------")
print("Baseline MAE :", baseline_mae)
print("Baseline RMSE:", baseline_rmse)
print("Baseline R²  :", baseline_r2)

print("\nCOMPARISON")
print("----------------------")
print("ML model MAE :", mae)
print("ML model RMSE:", rmse)
print("ML model R²  :", r2)


print("\n================================")
print("       MODEL RESULTS")
print("================================")

print("MAE :", mae)
print("RMSE:", rmse)
print("R²  :", r2)


# ==========================================
# 9. SAMPLE PREDICTIONS
# ==========================================

print("\nSample Predictions")
print("--------------------------------")

for i in range(10):

    print(
        f"Actual: {y_test[i]:.4f}"
        f" | Predicted: {y_pred[i]:.4f}"
    )