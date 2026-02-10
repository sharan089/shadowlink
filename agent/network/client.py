"""
HTTP Client
Communication with HQ server
"""

import requests
from utils.logger import setup_logger

logger = setup_logger(__name__)

class HQClient:
    """Client for communicating with HQ server"""
    
    def __init__(self, hq_url, api_key):
        self.hq_url = hq_url
        self.api_key = api_key
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {api_key}'
        }
    
    def register(self, agent_id):
        """Register with HQ"""
        url = f"{self.hq_url}/api/register"
        payload = {
            'agent_id': agent_id,
            'api_key': self.api_key
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info(f"Registered with HQ: {response.json()}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Registration failed: {e}")
            raise
    
    def send_heartbeat(self):
        """Send heartbeat to HQ"""
        url = f"{self.hq_url}/api/heartbeat"
        # Get agent_id from config or environment
        from config import AGENT_ID
        payload = {
            'agent_id': AGENT_ID
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Heartbeat failed: {e}")
            raise
    
    def get_commands(self):
        """Fetch pending commands from HQ"""
        from config import AGENT_ID
        url = f"{self.hq_url}/api/commands/{AGENT_ID}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get('commands', [])
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to fetch commands: {e}")
            return []
    
    def send_intel(self, intel_data):
        """Send intelligence data to HQ"""
        from config import AGENT_ID
        url = f"{self.hq_url}/api/intel"
        payload = {
            'agent_id': AGENT_ID,
            'data': intel_data
        }
        
        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to send intel: {e}")
            raise
