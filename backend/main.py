
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Locate the existing ML project files
PROJECT_ROOT = Path(__file__).resolve().parent.parent
ML_DIR = PROJECT_ROOT / "ml"
sys.path.insert(0, str(ML_DIR))

from water_calculation import (
    calculate_water_collection,
    calculate_tank_status,
    generate_recommendation,
)
from agent import water_management_agent
from genai import generate_ai_response
from predict_rainfall import predict_rainfall

app = FastAPI(title="SmartWaterAI API")

# Allow the frontend to connect during local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class WaterRequest(BaseModel):
    predicted_rainfall: float = Field(ge=0)
    roof_area: float = Field(gt=0)
    runoff_coefficient: float = Field(ge=0, le=1)
    current_water: float = Field(ge=0)
    tank_capacity: float = Field(gt=0)


@app.get("/")
def home():
    return {
        "message": "SmartWaterAI backend is running!",
        "docs": "/docs",
    }


@app.post("/api/analyze")
def analyze_water(data: WaterRequest):
    if data.current_water > data.tank_capacity:
        raise HTTPException(
            status_code=400,
            detail="Current water cannot exceed tank capacity.",
        )

    incoming_water = calculate_water_collection(
        data.predicted_rainfall,
        data.roof_area,
        data.runoff_coefficient,
    )

    stored_water, tank_percentage, overflow = calculate_tank_status(
        data.current_water,
        incoming_water,
        data.tank_capacity,
    )

    decision = water_management_agent(
        data.predicted_rainfall,
        tank_percentage,
        overflow,
        stored_water,
        data.tank_capacity,
    )

    recommendation = generate_ai_response(
        data.predicted_rainfall,
        incoming_water,
        tank_percentage,
        overflow,
        decision["decision"],
        decision["priority"],
    )

    return {
        "predicted_rainfall_mm": data.predicted_rainfall,
        "expected_rainwater_litres": round(incoming_water, 2),
        "current_water_litres": data.current_water,
        "water_after_rain_litres": round(stored_water, 2),
        "tank_capacity_litres": data.tank_capacity,
        "tank_level_percent": round(tank_percentage, 2),
        "overflow_litres": round(overflow, 2),
        "agent_decision": decision,
        "recommendation": recommendation,
    }

class RainfallRequest(BaseModel):
    state_code: int = Field(ge=1, le=38)
    forecast_date: str


@app.post("/api/predict-rainfall")
def predict_rainfall_api(data: RainfallRequest):
    try:
        result = predict_rainfall(
            state_code=data.state_code,
            forecast_date=data.forecast_date,
        )
        return result
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
