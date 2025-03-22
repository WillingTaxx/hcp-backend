import logging
from datetime import datetime

def setup_logger():
    """Configure and return a logger instance for the HCPR application"""
    
    # Create logger
    logger = logging.getLogger('hcpr')
    logger.setLevel(logging.INFO)
    
    # Create console handler and set level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Add formatter to console handler
    console_handler.setFormatter(formatter)
    
    # Add console handler to logger
    logger.addHandler(console_handler)
    
    return logger

# Create a global logger instance
logger = setup_logger()

def log_prediction(region: str, risk_score: float, risk_level: str):
    """Log prediction results"""
    logger.info(
        f"Prediction made for {region} - Risk Score: {risk_score:.2f}, "
        f"Risk Level: {risk_level}"
    )

def log_error(error_msg: str, additional_info: dict = None):
    """Log error messages with optional additional information"""
    if additional_info:
        logger.error(f"{error_msg} - Additional Info: {additional_info}")
    else:
        logger.error(error_msg)