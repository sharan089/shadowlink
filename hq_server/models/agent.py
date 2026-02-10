"""
Agent Data Model
Data structure for agent representation
"""

class Agent:
    """Represents a field agent"""
    
    def __init__(self, agent_id, api_key):
        self.agent_id = agent_id
        self.api_key = api_key
        self.status = "offline"
        self.last_heartbeat = None
        self.metadata = {}
