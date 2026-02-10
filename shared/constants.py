"""
Protocol Constants
Status codes and command names
"""

# Agent Status
AGENT_STATUS_ONLINE = "online"
AGENT_STATUS_OFFLINE = "offline"
AGENT_STATUS_IDLE = "idle"
AGENT_STATUS_EXECUTING = "executing"

# Command Status
COMMAND_PENDING = "pending"
COMMAND_EXECUTING = "executing"
COMMAND_COMPLETED = "completed"
COMMAND_FAILED = "failed"

# HTTP Status Codes
STATUS_OK = 200
STATUS_CREATED = 201
STATUS_BAD_REQUEST = 400
STATUS_UNAUTHORIZED = 401
STATUS_NOT_FOUND = 404
STATUS_SERVER_ERROR = 500

# Command Types
COMMAND_EXEC = "exec"
COMMAND_QUERY = "query"
COMMAND_SHUTDOWN = "shutdown"
COMMAND_HEARTBEAT = "heartbeat"
