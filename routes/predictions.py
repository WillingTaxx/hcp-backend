from fastapi import APIRouter, HTTPException
from models.famine_model import FamineModel
from schemas.prediction import FamineRequest, FamineResponse
from utils.logger import logger, log_error

router = APIRouter(tags=["predictions"])

# Initialize the famine prediction model
famine_model = FamineModel()

@router.post("/predict_famine", response_model=FamineResponse)
async def predict_famine(request: FamineRequest):
    """
    Endpoint to predict famine risk based on input parameters
    """
    try:
        logger.info(f"Received famine prediction request for region: {request.region}")
        
        # Generate prediction using the famine model
        prediction = famine_model.predict(request)
        
        logger.info(f"Successfully generated prediction for region: {request.region}")
        return prediction
        
    except Exception as e:
        error_msg = f"Error processing famine prediction request: {str(e)}"
        log_error(error_msg, {"region": request.region})
        raise HTTPException(
            status_code=500,
            detail=error_msg
        )
