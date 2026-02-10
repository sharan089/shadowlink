"""
HQ Server Configuration
Port, intervals, and other settings
"""

# Server settings
HQ_HOST = "0.0.0.0"
HQ_PORT = 5000
DEBUG = True

# Heartbeat and timeout settings
HEARTBEAT_TIMEOUT = 60  # seconds
HEARTBEAT_INTERVAL = 30  # seconds

# Database/Storage settings
STORAGE_PATH = "./data"

# Security settings
API_KEY_LENGTH = 32
