"""
Communication Protocol
Message formats and JSON schemas for agent-HQ communication
"""

from typing import Dict, Any

class MessageProtocol:
    """Defines message formats for communication"""
    
    @staticmethod
    def register_message(agent_id: str, metadata: Dict[str, Any]) -> Dict:
        """Create agent registration message"""
        return {
            "type": "register",
            "agent_id": agent_id,
            "metadata": metadata
        }
    
    @staticmethod
    def heartbeat_message(agent_id: str) -> Dict:
        """Create heartbeat message"""
        return {
            "type": "heartbeat",
            "agent_id": agent_id,
            "timestamp": None
        }
    
    @staticmethod
    def command_message(command_id: str, command_type: str, payload: Dict) -> Dict:
        """Create command message"""
        return {
            "type": "command",
            "command_id": command_id,
            "command_type": command_type,
            "payload": payload
        }
