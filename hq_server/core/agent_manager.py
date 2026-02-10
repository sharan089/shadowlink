"""
Agent Manager
Tracks agent status (online/offline) and metadata
"""

from datetime import datetime

class AgentManager:
    """Manages agent connections and status"""
    
    def __init__(self):
        self.agents = {}
    
    def register_agent(self, agent_id, metadata):
        """Register a new agent"""
        self.agents[agent_id] = {
            'agent_id': agent_id,
            'status': 'online',
            'metadata': metadata,
            'last_heartbeat': datetime.utcnow().isoformat(),
            'registered_at': datetime.utcnow().isoformat()
        }
    
    def mark_online(self, agent_id):
        """Mark agent as online"""
        if agent_id in self.agents:
            self.agents[agent_id]['status'] = 'online'
            self.agents[agent_id]['last_heartbeat'] = datetime.utcnow().isoformat()
    
    def mark_offline(self, agent_id):
        """Mark agent as offline"""
        if agent_id in self.agents:
            self.agents[agent_id]['status'] = 'offline'
    
    def get_all_agents(self):
        """Get all agents"""
        return list(self.agents.values())
