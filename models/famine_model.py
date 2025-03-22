from typing import List, Tuple
from hcp_backend.schemas.prediction import FamineRequest, FamineResponse
from hcp_backend.utils.logger import log_prediction, log_error

class FamineModel:
    # Define weights for different factors (can be adjusted based on domain expertise)
    WEIGHTS = {
        'rainfall_mm': 0.12,
        'temperature_c': 0.08,
        'humidity_percent': 0.05,
        'crop_yield_tons': 0.15,
        'food_price_index': 0.12,
        'food_stock_tons': 0.13,
        'gdp_per_capita': 0.08,
        'unemployment_rate': 0.09,
        'inflation_rate': 0.08,
        'ndvi_index': 0.05,
        'soil_moisture': 0.05
    }

    # Risk level thresholds
    RISK_THRESHOLDS = {
        'LOW': 30,
        'MEDIUM': 60,
        'HIGH': 100
    }

    def __init__(self):
        # Initialize any required resources
        pass

    def _normalize_value(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize a value to a 0-100 scale"""
        return ((value - min_val) / (max_val - min_val)) * 100

    def _calculate_risk_score(self, data: FamineRequest) -> float:
        """Calculate the risk score based on weighted inputs"""
        score = 0.0
        
        # Normalize and weight each factor
        # Note: These normalizations are simplified and should be adjusted based on real-world ranges
        score += self.WEIGHTS['rainfall_mm'] * (1 - self._normalize_value(data.rainfall_mm, 0, 1000))
        score += self.WEIGHTS['temperature_c'] * self._normalize_value(data.temperature_c, -10, 50)
        score += self.WEIGHTS['humidity_percent'] * (1 - data.humidity_percent / 100)
        score += self.WEIGHTS['crop_yield_tons'] * (1 - self._normalize_value(data.crop_yield_tons, 0, 1000))
        score += self.WEIGHTS['food_price_index'] * self._normalize_value(data.food_price_index, 0, 200)
        score += self.WEIGHTS['food_stock_tons'] * (1 - self._normalize_value(data.food_stock_tons, 0, 1000))
        score += self.WEIGHTS['gdp_per_capita'] * (1 - self._normalize_value(data.gdp_per_capita, 0, 100000))
        score += self.WEIGHTS['unemployment_rate'] * (data.unemployment_rate / 100)
        score += self.WEIGHTS['inflation_rate'] * self._normalize_value(data.inflation_rate, 0, 50)
        score += self.WEIGHTS['ndvi_index'] * (1 - ((data.ndvi_index + 1) / 2))
        score += self.WEIGHTS['soil_moisture'] * (1 - data.soil_moisture / 100)

        return min(max(score * 100, 0), 100)  # Ensure score is between 0 and 100

    def _determine_risk_level(self, risk_score: float) -> str:
        """Determine risk level based on risk score"""
        if risk_score <= self.RISK_THRESHOLDS['LOW']:
            return 'LOW'
        elif risk_score <= self.RISK_THRESHOLDS['MEDIUM']:
            return 'MEDIUM'
        else:
            return 'HIGH'

    def _identify_contributing_factors(self, data: FamineRequest, risk_score: float) -> List[str]:
        """Identify top 3 factors contributing to the risk"""
        factor_contributions = [
            ("Low rainfall", self.WEIGHTS['rainfall_mm'] * (1 - self._normalize_value(data.rainfall_mm, 0, 1000))),
            ("High temperature", self.WEIGHTS['temperature_c'] * self._normalize_value(data.temperature_c, -10, 50)),
            ("Low crop yield", self.WEIGHTS['crop_yield_tons'] * (1 - self._normalize_value(data.crop_yield_tons, 0, 1000))),
            ("High food prices", self.WEIGHTS['food_price_index'] * self._normalize_value(data.food_price_index, 0, 200)),
            ("Low food stocks", self.WEIGHTS['food_stock_tons'] * (1 - self._normalize_value(data.food_stock_tons, 0, 1000))),
            ("High unemployment", self.WEIGHTS['unemployment_rate'] * (data.unemployment_rate / 100)),
            ("High inflation", self.WEIGHTS['inflation_rate'] * self._normalize_value(data.inflation_rate, 0, 50))
        ]
        
        # Sort factors by their contribution to risk score
        sorted_factors = sorted(factor_contributions, key=lambda x: x[1], reverse=True)
        return [factor[0] for factor in sorted_factors[:3]]

    def _get_recommended_actions(self, risk_level: str, contributing_factors: List[str]) -> List[str]:
        """Generate recommended actions based on risk level and contributing factors"""
        actions = []
        
        if "Low rainfall" in contributing_factors or "High temperature" in contributing_factors:
            actions.append("Implement drought-resistant farming techniques and irrigation systems")
        
        if "Low crop yield" in contributing_factors:
            actions.append("Distribute improved seeds and agricultural inputs to farmers")
        
        if "High food prices" in contributing_factors or "Low food stocks" in contributing_factors:
            actions.append("Establish emergency food reserves and price stabilization measures")
        
        if "High unemployment" in contributing_factors or "High inflation" in contributing_factors:
            actions.append("Implement emergency employment programs and economic stabilization measures")
        
        # Add general recommendations based on risk level
        if risk_level == "HIGH":
            actions.append("Activate emergency response protocols and seek international assistance")
        
        return actions[:5]  # Return up to 5 recommendations

    def predict(self, data: FamineRequest) -> FamineResponse:
        """Generate famine prediction based on input data"""
        try:
            # Calculate risk score
            risk_score = self._calculate_risk_score(data)
            
            # Determine risk level
            risk_level = self._determine_risk_level(risk_score)
            
            # Identify contributing factors
            contributing_factors = self._identify_contributing_factors(data, risk_score)
            
            # Get recommended actions
            recommended_actions = self._get_recommended_actions(risk_level, contributing_factors)
            
            # Create response
            response = FamineResponse(
                region=data.region,
                risk_score=risk_score,
                risk_level=risk_level,
                contributing_factors=contributing_factors,
                recommended_actions=recommended_actions
            )
            
            # Log the prediction
            log_prediction(data.region, risk_score, risk_level)
            
            return response
            
        except Exception as e:
            log_error(f"Error in famine prediction: {str(e)}", {
                "region": data.region,
                "error_type": type(e).__name__
            })
            raise