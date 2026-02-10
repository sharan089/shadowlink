"""
Time Utilities
Timestamp and timeout utilities
"""

from datetime import datetime

def get_current_timestamp():
    """Get current timestamp"""
    return datetime.utcnow().isoformat()

def is_timeout(last_time, timeout_seconds):
    """Check if timeout has been exceeded"""
    pass
