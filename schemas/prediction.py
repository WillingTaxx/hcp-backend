from datetime import datetime
from typing import List
from pydantic import BaseModel, Field

class FamineRequest(BaseModel):
    region: str = Field(..., description="Geographic region for prediction")
    rainfall_mm: float = Field(..., description="Average rainfall in millimeters")
    temperature_c: float = Field(..., description="Average temperature in Celsius")
    humidity_percent: float = Field(..., ge=0, le=100, description="Humidity percentage")
    crop_yield_tons: float = Field(..., ge=0, description="Crop yield in tons")
    food_price_index: float = Field(..., ge=0, description="Food price index")
    food_stock_tons: float = Field(..., ge=0, description="Food stock in tons")
    gdp_per_capita: float = Field(..., ge=0, description="GDP per capita")
    unemployment_rate: float = Field(..., ge=0, le=100, description="Unemployment rate percentage")
    inflation_rate: float = Field(..., description="Inflation rate percentage")
    ndvi_index: float = Field(..., ge=-1, le=1, description="Normalized Difference Vegetation Index")
    soil_moisture: float = Field(..., ge=0, le=100, description="Soil moisture percentage")

class FamineResponse(BaseModel):
    region: str
    risk_score: float = Field(..., ge=0, le=100, description="Calculated risk score")
    risk_level: str = Field(..., description="Risk level: LOW, MEDIUM, or HIGH")
    contributing_factors: List[str] = Field(..., min_items=1, max_items=3, description="Top factors contributing to risk")
    recommended_actions: List[str] = Field(..., min_items=3, max_items=5, description="Recommended response actions")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Timestamp of prediction")

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }