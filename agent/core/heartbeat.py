"""
Agent Heartbeat
Sends periodic heartbeat to HQ
"""

class Heartbeat:
    """Handles agent heartbeat"""
    
    def __init__(self, interval=30):
        self.interval = interval
    
    def send_heartbeat(self, hq_client):
        """Send heartbeat to HQ"""
        pass
