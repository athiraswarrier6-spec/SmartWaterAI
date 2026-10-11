# ==========================================
# SMARTWATERAI - GENAI RECOMMENDATION
# ==========================================

def generate_ai_response(
    predicted_rainfall,
    incoming_water,
    tank_percentage,
    overflow,
    decision,
    priority
):

    if decision == "OVERFLOW_RISK":
        response = (
            f"Heavy rainfall is expected. Approximately "
            f"{incoming_water:.2f} litres of rainwater may "
            f"be collected. The tank is at "
            f"{tank_percentage:.2f}% capacity. "
            f"Overflow risk is present. Use stored water "
            f"and divert excess water safely."
        )

    elif decision == "LOW_WATER":
        response = (
            f"Water availability is low. The tank level is "
            f"{tank_percentage:.2f}%. Conserve water and "
            f"reduce non-essential usage."
        )

    elif decision == "LOW_RAINFALL":
        response = (
            f"Only {predicted_rainfall:.2f} mm of rainfall "
            f"is expected. Approximately "
            f"{incoming_water:.2f} litres may be collected. "
            f"Use stored water carefully and conserve water."
        )

    elif decision == "HIGH_WATER":
        response = (
            f"The tank is at {tank_percentage:.2f}% capacity. "
            f"Monitor the tank because additional rainfall "
            f"may cause overflow."
        )

    else:
        response = (
            f"SmartWaterAI predicts {predicted_rainfall:.2f} mm "
            f"of rainfall and approximately "
            f"{incoming_water:.2f} litres of rainwater "
            f"collection. The expected tank level is "
            f"{tank_percentage:.2f}%. There is currently "
            f"no overflow risk. Continue normal water "
            f"management."
        )

    return {
        "priority": priority,
        "response": response
    }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    result = generate_ai_response(
        predicted_rainfall=5.87,
        incoming_water=469.21,
        tank_percentage=29.38,
        overflow=0,
        decision="NORMAL",
        priority="LOW"
    )

    print("\n==========================================")
    print("       SMARTWATERAI GENAI")
    print("==========================================")

    print("Priority :", result["priority"])

    print("\nAI Recommendation:")
    print(result["response"])

    print("==========================================")