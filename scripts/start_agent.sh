#!/bin/bash
# Start Field Agent

echo "Starting ShadowLink Field Agent..."

cd "$(dirname "$0")/../agent" || exit 1

# Install dependencies if needed
pip install -r requirements.txt

# Start the agent
python agent.py
