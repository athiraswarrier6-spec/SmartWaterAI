# ==========================================
# SMARTWATERAI - WATER COLLECTION CALCULATOR
# ==========================================

def calculate_water_collection(
    rainfall_mm,
    roof_area_m2,
    runoff_coefficient=0.8
):
    """
    Calculate the amount of rainwater that can be harvested.

    Formula:
    Water collected (litres)
    = Rainfall (mm) × Roof area (m²) × Runoff coefficient
    """

    water_collected = (
        rainfall_mm
        * roof_area_m2
        * runoff_coefficient
    )

    return water_collected


def calculate_tank_status(
    current_water,
    incoming_water,
    tank_capacity
):
    """
    Calculate the future tank level.
    """

    total_water = current_water + incoming_water

    # Prevent tank level from exceeding capacity
    stored_water = min(total_water, tank_capacity)

    tank_percentage = (
        stored_water / tank_capacity
    ) * 100

    overflow = max(
        total_water - tank_capacity,
        0
    )

    return stored_water, tank_percentage, overflow


def generate_recommendation(
    tank_percentage,
    overflow,
    predicted_rainfall
):
    """
    Generate a simple water-management recommendation.
    """

    if overflow > 0:
        return (
            "Tank may overflow. "
            "Use the stored water for suitable purposes."
        )

    elif tank_percentage < 20:
        return (
            "Water level is low. "
            "Conserve water and reduce non-essential usage."
        )

    elif predicted_rainfall < 5:
        return (
            "Low rainfall is expected. "
            "Use stored water carefully."
        )

    elif tank_percentage > 80:
        return (
            "Tank level is high. "
            "Continue monitoring water usage."
        )

    else:
        return (
            "Water availability is sufficient. "
            "Continue normal water management."
        )


# ==========================================
# TEST THE CALCULATOR
# ==========================================

if __name__ == "__main__":

    # Example inputs
    predicted_rainfall = 20       # mm
    roof_area = 100               # square metres
    runoff_coefficient = 0.8

    current_water = 1000          # litres
    tank_capacity = 5000          # litres

    # Calculate incoming rainwater
    incoming_water = calculate_water_collection(
        predicted_rainfall,
        roof_area,
        runoff_coefficient
    )

    # Calculate future tank status
    stored_water, tank_percentage, overflow = calculate_tank_status(
        current_water,
        incoming_water,
        tank_capacity
    )

    # Generate recommendation
    recommendation = generate_recommendation(
        tank_percentage,
        overflow,
        predicted_rainfall
    )

    print("\n===================================")
    print("       SMARTWATERAI")
    print("   WATER MANAGEMENT SYSTEM")
    print("===================================")

    print(f"Predicted Rainfall : {predicted_rainfall:.2f} mm")
    print(f"Roof Area         : {roof_area:.2f} m²")
    print(f"Current Water     : {current_water:.2f} L")
    print(f"Incoming Water    : {incoming_water:.2f} L")
    print(f"Tank Capacity     : {tank_capacity:.2f} L")
    print(f"Stored Water      : {stored_water:.2f} L")
    print(f"Tank Level        : {tank_percentage:.2f}%")
    print(f"Overflow          : {overflow:.2f} L")

    print("\nRecommendation:")
    print(recommendation)