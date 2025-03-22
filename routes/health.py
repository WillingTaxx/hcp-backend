from fastapi import APIRouter
from hcp_backend.utils.logger import logger

router = APIRouter(tags=["health"])

@router.get("/")
async def health_check():
    """
    Health check endpoint to verify API status
    """
    logger.info("Health check request received")
    return {
        "message": "HCPR API is running",
        "version": "1.0.0"
    }