"""
Command Data Model
Data structure for commands
"""

class Command:
    """Represents a command to be executed"""
    
    def __init__(self, command_id, agent_id, command_type, payload):
        self.command_id = command_id
        self.agent_id = agent_id
        self.command_type = command_type
        self.payload = payload
        self.status = "pending"
        self.created_at = None
