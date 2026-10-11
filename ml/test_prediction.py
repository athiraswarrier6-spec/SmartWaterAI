
import csv
from pathlib import Path

dataset = (
    Path(__file__).resolve().parent.parent
    / "data"
    / "daily-rainfall-at-state-level.csv"
)

states = {}

with open(dataset, "r", encoding="utf-8") as file:
    for row in csv.DictReader(file):
        try:
            code = int(row["state_code"])
            name = row["state_name"]
            states[code] = name
        except (ValueError, TypeError):
            continue

print("Available states:")
for code, name in sorted(states.items()):
    print(f"Code: {code} | State: {name}")
