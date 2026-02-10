"""
Command Queue
Stores and manages pending commands for agents
"""

class CommandQueue:
    """Queue for managing pending commands"""
    
    def __init__(self):
        self.queue = {}  # agent_id -> [commands]
    
    def enqueue(self, agent_id, command):
        """Add command to queue"""
        if agent_id not in self.queue:
            self.queue[agent_id] = []
        self.queue[agent_id].append(command)
    
    def dequeue(self, agent_id):
        """Get all commands for agent"""
        if agent_id in self.queue:
            commands = self.queue[agent_id]
            self.queue[agent_id] = []  # Clear the queue
            return commands
        return []
