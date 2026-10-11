# ==========================================
# SMARTWATERAI - AGENTIC AI
# ==========================================

def water_management_agent(
    predicted_rainfall,
    tank_percentage,
    overflow,
    current_water,
    tank_capacity
):
    """
    Agent analyzes the current water situation
    and decides the best water-management action.
    """

    # --------------------------------------
    # Decision 1: Overflow
    # --------------------------------------

    if overflow > 0:

        decision = "OVERFLOW_RISK"

        action = (
            "Use the stored water and divert excess "
            "rainwater to a safe recharge or storage area."
        )

        priority = "HIGH"

    # --------------------------------------
    # Decision 2: Very low tank
    # --------------------------------------

    elif tank_percentage < 20:

        decision = "LOW_WATER"

        action = (
            "Conserve water, reduce non-essential usage, "
            "and prepare for low water availability."
        )

        priority = "HIGH"

    # --------------------------------------
    # Decision 3: Low rainfall
    # --------------------------------------

    elif predicted_rainfall < 5:

        decision = "LOW_RAINFALL"

        action = (
            "Rainfall is expected to be low. "
            "Use stored water carefully and conserve water."
        )

        priority = "MEDIUM"

    # --------------------------------------
    # Decision 4: High tank level
    # --------------------------------------

    elif tank_percentage > 80:

        decision = "HIGH_WATER"

        action = (
            "Tank level is high. Monitor the tank and "
            "prepare for possible overflow during heavy rainfall."
        )

        priority = "MEDIUM"

    # --------------------------------------
    # Decision 5: Normal condition
    # --------------------------------------

    else:

        decision = "NORMAL"

        action = (
            "Water availability is sufficient. "
            "Continue normal water management."
        )

        priority = "LOW"


    # --------------------------------------
    # Agent output
    # --------------------------------------

    return {
        "decision": decision,
        "priority": priority,
        "action": action,
        "tank_percentage": tank_percentage,
        "predicted_rainfall": predicted_rainfall,
        "current_water": current_water,
        "tank_capacity": tank_capacity
    }


# ==========================================
# TEST AGENT
# ==========================================

if __name__ == "__main__":

    result = water_management_agent(
        predicted_rainfall=5.87,
        tank_percentage=29.38,
        overflow=0,
        current_water=1000,
        tank_capacity=5000
    )

    print("\n==========================================")
    print("       SMARTWATERAI AGENT")
    print("==========================================")

    print("Decision :", result["decision"])
    print("Priority :", result["priority"])
    print("Action   :", result["action"])

    print("------------------------------------------")

    print(
        f"Predicted Rainfall : "
        f"{result['predicted_rainfall']:.2f} mm"
    )

    print(
        f"Tank Level : "
        f"{result['tank_percentage']:.2f}%"
    )

    print("==========================================")