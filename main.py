from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from routes import health, predictions
from hcp_backend.utils.logger import logger, log_error

# Initialize FastAPI app
app = FastAPI(
    title="HCPR API",
    description="Humanitarian Crisis Prediction & Response API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="")
app.include_router(predictions.router, prefix="/api/v1")

@app.on_event("startup")
async def startup_event():
    """
    Runs when the application starts
    """
    logger.info("HCPR API starting up...")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the application is shutting down
    """
    logger.info("HCPR API shutting down...")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """
    Handle HTTP exceptions
    """
    log_error(f"HTTP error occurred: {exc.detail}", {
        "status_code": exc.status_code,
        "path": request.url.path
    })
    return {"detail": exc.detail, "status_code": exc.status_code}

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """
    Handle general exceptions
    """
    error_msg = f"Unexpected error occurred: {str(exc)}"
    log_error(error_msg, {"path": request.url.path})
    return {"detail": error_msg, "status_code": 500}
