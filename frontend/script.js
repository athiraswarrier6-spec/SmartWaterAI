
const waterForm = document.getElementById("waterForm");
const analyzeButton = document.getElementById("analyzeButton");
const statusMessage = document.getElementById("status");
const results = document.getElementById("results");

waterForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const requestData = {
        predicted_rainfall: Number(document.getElementById("rainfall").value),
        roof_area: Number(document.getElementById("roof").value),
        runoff_coefficient: Number(document.getElementById("runoff").value),
        current_water: Number(document.getElementById("currentWater").value),
        tank_capacity: Number(document.getElementById("capacity").value)
    };

    statusMessage.textContent = "";
    results.hidden = true;
    analyzeButton.disabled = true;
    analyzeButton.textContent = "Analyzing...";

    try {
        const response = await fetch("http://127.0.0.1:8000/api/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.detail
                    ? (typeof data.detail === "string"
                        ? data.detail
                        : JSON.stringify(data.detail))
                    : "Unable to analyze water."
            );
        }

        document.getElementById("incoming").textContent =
            Number(data.expected_rainwater_litres).toLocaleString("en-IN");

        document.getElementById("stored").textContent =
            Number(data.water_after_rain_litres).toLocaleString("en-IN");

        document.getElementById("level").textContent =
            data.tank_level_percent + "%";

        document.getElementById("overflow").textContent =
            Number(data.overflow_litres).toLocaleString("en-IN");

        document.getElementById("progress").style.width =
            Math.min(100, Math.max(0, data.tank_level_percent)) + "%";
            
document.getElementById("tankWater").style.height =
    Math.min(100, Math.max(0, data.tank_level_percent)) + "%";

document.getElementById("tankLabel").textContent =
    data.tank_level_percent + "%";


        document.getElementById("decision").textContent =
            data.agent_decision.decision +
            " (Priority: " + data.agent_decision.priority + ")";

        document.getElementById("action").textContent =
            data.agent_decision.action;

        document.getElementById("recommendation").textContent =
            data.recommendation.response;

        results.hidden = false;
        statusMessage.textContent = "";
        results.scrollIntoView({ behavior: "smooth", block: "start" });

    } catch (error) {
        statusMessage.textContent =
            "Could not connect to SmartWaterAI. Make sure the backend is running. " +
            error.message;
    } finally {
        analyzeButton.disabled = false;
        analyzeButton.textContent = "Analyze Water";
    }
});

const predictRainfallButton = document.getElementById("predictRainfallButton");
const predictionStatus = document.getElementById("predictionStatus");
const forecastDateInput = document.getElementById("forecastDate");

// Set tomorrow as the default prediction date.
const tomorrow = new Date();
tomorrow.setDate(tomorrow.getDate() + 1);
forecastDateInput.value =
    `${tomorrow.getFullYear()}-${String(tomorrow.getMonth() + 1).padStart(2, "0")}-${String(tomorrow.getDate()).padStart(2, "0")}`;

predictRainfallButton.addEventListener("click", async function () {
    const stateCode = Number(document.getElementById("stateCode").value);
    const forecastDate = forecastDateInput.value;

    if (!forecastDate) {
        predictionStatus.textContent = "Please select a date.";
        return;
    }

    predictionStatus.textContent = "Estimating rainfall...";
    predictRainfallButton.disabled = true;

    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/predict-rainfall",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    state_code: stateCode,
                    forecast_date: forecastDate
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Rainfall prediction failed.");
        }

        // Fill the rainfall input in the existing water-analysis form.
        document.getElementById("rainfall").value =
            data.estimated_rainfall_mm;

        predictionStatus.textContent =
            `Estimated rainfall: ${data.estimated_rainfall_mm} mm for ` +
            `${data.forecast_date}. ${data.note}`;

    } catch (error) {
        predictionStatus.textContent =
            "Could not get the rainfall estimate: " + error.message;
    } finally {
        predictRainfallButton.disabled = false;
    }
});
