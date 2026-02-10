"""
Agent Configuration
Settings for agent behavior
"""

# HQ Server settings
HQ_URL = "http://127.0.0.1:5000"


# Agent settings
AGENT_ID = "agent_001"
API_KEY = ""  # Set from environment or config

# Timing settings
HEARTBEAT_INTERVAL = 30  # seconds
CHECK_COMMANDS_INTERVAL = 10  # seconds

# Retry settings
MAX_RETRIES = 5
BASE_RETRY_DELAY = 2
