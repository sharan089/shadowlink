"""
Field Agent Entry Point
Main agent loop for command execution and data collection
"""

import time
import os
from config import HQ_URL, AGENT_ID, HEARTBEAT_INTERVAL, API_KEY
from network.client import HQClient
from utils.logger import setup_logger

logger = setup_logger(__name__)

def main():
    """Main agent loop"""
    
    # Use environment variable for API key if available
    api_key = os.getenv('AGENT_API_KEY', API_KEY or 'default_key')
    
    client = HQClient(HQ_URL, api_key)
    
    logger.info(f"Registering agent {AGENT_ID} with HQ at {HQ_URL}")
    
    try:
        # Register with HQ
        client.register(AGENT_ID)
        logger.info("Successfully registered with HQ")
    except Exception as e:
        logger.error(f"Failed to register: {e}")
        return
    
    # Main loop
    logger.info(f"Starting heartbeat loop (interval: {HEARTBEAT_INTERVAL}s)")
    
    try:
        while True:
            try:
                # Send heartbeat
                client.send_heartbeat()
                logger.info("Heartbeat sent")
                
                # Check for commands
                commands = client.get_commands()
                if commands:
                    logger.info(f"Received {len(commands)} command(s)")
                    for cmd in commands:
                        logger.info(f"Command: {cmd}")
                
                # Wait before next heartbeat
                time.sleep(HEARTBEAT_INTERVAL)
                
            except Exception as e:
                logger.error(f"Error in agent loop: {e}")
                time.sleep(HEARTBEAT_INTERVAL)
    
    except KeyboardInterrupt:
        logger.info("Agent shutting down")

if __name__ == "__main__":
    main()
