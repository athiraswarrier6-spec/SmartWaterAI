# SmartWaterAI

## AI-Based Predictive Rainwater Harvesting and Smart Water Management System



### 1. Project Overview

SmartWaterAI is an AI/ML-supported web application designed to estimate rainfall, calculate potential rainwater collection, monitor tank storage, identify possible overflow, and provide water-management recommendations.



The project aims to promote efficient rainwater harvesting and support Sustainable Development Goal 6 (Clean Water and Sanitation).



### 2. Objectives

 Estimate rainfall for a selected state and date using an experimental ML model.

 Calculate rainwater collected from a rooftop.

 Estimate tank storage, fill percentage, and possible overflow.

 Provide recommendations for effective water management.

 Encourage water conservation and reduce water wastage.



### 3. Main Features

 Rainfall estimation by state and date.

 Rainwater collection calculator.

 Tank capacity and overflow analysis.

 Water-management decision agent.

 Interactive web dashboard.

 Backend API for rainfall prediction and water analysis.



### 4. Technologies Used

 Frontend: HTML, CSS, JavaScript

 Backend: Python and FastAPI

 Machine Learning: NumPy and linear regression

 Dataset: Daily rainfall data at state level

 Development tools: Visual Studio Code, Git and GitHub



### 5. Project Structure

 backend: Contains the FastAPI application.

 data: Contains the rainfall dataset.

 frontend: Contains the dashboard files.

 ml: Contains the machine-learning model and water-management logic.



### 6. Working

1. The user selects a state and forecast date.

2. The system generates an experimental rainfall estimate.

3. The user enters roof area, runoff coefficient, current tank water, and tank capacity.

4. The backend calculates potential collected water, tank storage, and overflow.

5. The decision agent provides a suitable water-management recommendation.



### 7. Water Collection Formula

Collected water (litres) = Rainfall (mm) × Roof area (m²) × Runoff coefficient.



For example, with 20 mm rainfall, a 100 m² roof, and a runoff coefficient of 0.8:



Collected water = 20 × 100 × 0.8 = 1,600 litres.



### 8. Machine Learning Results

The current experimental model achieved the following overall test results:



 Mean Absolute Error (MAE): 4.14 mm

 Root Mean Squared Error (RMSE): 8.84 mm

 R² Score: 0.229



These results indicate that the model needs further improvement and validation.



## 9. Limitations

 Rainfall predictions are experimental estimates, not official weather forecasts.

 The current system does not use live tank-level sensors.

 The rainfall model requires further validation to improve reliability.



### 10. Future Scope

 Integrate an official weather API.

 Improve the machine-learning model.

 Add IoT sensors for real-time tank monitoring.

 Deploy the web application for wider use.

 Improve water-demand prediction and recommendations.



### 11. Social Impact

SmartWaterAI aims to support rainwater harvesting, reduce water wastage, improve water-use planning, and contribute to SDG 6: Clean Water and Sanitation.



### 12. Conclusion

SmartWaterAI combines experimental rainfall estimation, rainwater collection calculations, tank-status analysis, and recommendation logic in one web application. The working prototype provides a foundation for developing a more reliable and intelligent rainwater management system.



### 13. Author Details

Name: Athira S



Department: BTech Artificial Intelligence and Machine Learning



College: Vidya Academy of Science and Technology

### Important Note

The rainfall output is an experimental model estimate and should not be treated as an official weather forecast.



