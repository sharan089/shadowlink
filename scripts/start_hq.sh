#!/bin/bash
# Start HQ Server

echo "Starting ShadowLink HQ Server..."

cd "$(dirname "$0")/../hq_server" || exit 1

# Install dependencies if needed
pip install -r requirements.txt

# Start the server
python main.py
