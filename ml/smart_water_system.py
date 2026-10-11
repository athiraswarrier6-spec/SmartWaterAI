# ==========================================
# SMARTWATERAI - COMPLETE AI SYSTEM
# ML + WATER CALCULATION + AGENT
# ==========================================

import runpy

from water_calculation import (
    calculate_water_collection,
    calculate_tank_status
)

from agent import water_management_agent
from genai import generate_ai_response

# ==========================================
# 1. RUN ML MODEL
# ==========================================

print("\nRunning rainfall prediction model...\n")

ml_results = runpy.run_path("ml/train_model.py")

y_pred = ml_results["y_pred"]

predicted_rainfall = float(y_pred[0])

# Rainfall cannot be negative
predicted_rainfall = max(predicted_rainfall, 0)


# ==========================================
# 2. HOUSE / TANK INFORMATION
# ==========================================

roof_area = 100
runoff_coefficient = 0.8

current_water = 1000
tank_capacity = 5000


# ==========================================
# 3. CALCULATE EXPECTED RAINWATER
# ==========================================

incoming_water = calculate_water_collection(
    predicted_rainfall,
    roof_area,
    runoff_coefficient
)


# ==========================================
# 4. CALCULATE TANK STATUS
# ==========================================

stored_water, tank_percentage, overflow = calculate_tank_status(
    current_water,
    incoming_water,
    tank_capacity
)


# ==========================================
# 5. AGENT MAKES DECISION
# ==========================================

agent_result = water_management_agent(
    predicted_rainfall=predicted_rainfall,
    tank_percentage=tank_percentage,
    overflow=overflow,
    current_water=current_water,
    tank_capacity=tank_capacity
)


# ==========================================
# 6. DISPLAY COMPLETE SMARTWATERAI RESULT
# ==========================================

print("\n==========================================")
print("          SMARTWATERAI SYSTEM")
print("==========================================")

print(f"Predicted Rainfall : {predicted_rainfall:.2f} mm")
print(f"Roof Area          : {roof_area:.2f} m²")
print(f"Current Water      : {current_water:.2f} L")

print("------------------------------------------")

print(f"Expected Rainwater : {incoming_water:.2f} L")
print(f"Tank Capacity      : {tank_capacity:.2f} L")
print(f"Water After Rain   : {stored_water:.2f} L")
print(f"Tank Level         : {tank_percentage:.2f}%")
print(f"Overflow           : {overflow:.2f} L")

print("------------------------------------------")

print("AGENT DECISION")
print("------------------------------------------")

print(f"Decision : {agent_result['decision']}")
print(f"Priority : {agent_result['priority']}")
print(f"Action   : {agent_result['action']}")

# ==========================================
# 7. GENAI RECOMMENDATION
# ==========================================

genai_result = generate_ai_response(
    predicted_rainfall=predicted_rainfall,
    incoming_water=incoming_water,
    tank_percentage=tank_percentage,
    overflow=overflow,
    decision=agent_result["decision"],
    priority=agent_result["priority"]
)

print("------------------------------------------")
print("GENAI RECOMMENDATION")
print("------------------------------------------")

print(genai_result["response"])

print("==========================================")