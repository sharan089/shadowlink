# ShadowLink Protocol

## Message Format
All messages are JSON-based with the following structure:

```json
{
  "type": "message_type",
  "agent_id": "agent_001",
  "timestamp": "2026-02-10T12:00:00Z",
  "payload": {}
}
```

## Message Types

### Registration
Agent registers with HQ:
```json
{
  "type": "register",
  "agent_id": "agent_001",
  "metadata": {
    "hostname": "target_host",
    "os": "Windows"
  }
}
```

### Heartbeat
Agent sends heartbeat:
```json
{
  "type": "heartbeat",
  "agent_id": "agent_001",
  "status": "online"
}
```

### Command
HQ sends command:
```json
{
  "type": "command",
  "command_id": "cmd_001",
  "command_type": "exec",
  "payload": {
    "command": "whoami"
  }
}
```

### Intelligence
Agent sends intelligence:
```json
{
  "type": "intel",
  "agent_id": "agent_001",
  "data": {
    "system_info": {},
    "network_info": {}
  }
}
```

## Status Codes
- 200 OK
- 201 Created
- 400 Bad Request
- 401 Unauthorized
- 404 Not Found
- 500 Server Error
