"""
Logging Utilities
Centralized logging for the HQ server
"""

import logging

def setup_logger(name):
    """Setup logger with standard configuration"""
    logger = logging.getLogger(name)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger
