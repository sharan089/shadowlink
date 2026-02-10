"""
Logging Utilities
Centralized logging for the agent
"""

import logging

def setup_logger(name):
    """Setup logger with standard configuration"""
    logger = logging.getLogger(name)
    
    # Only add handler if not already added
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    
    return logger
