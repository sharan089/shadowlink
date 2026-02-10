# ShadowLink Protocol Specification

**Version:** 1.0  
**Last Updated:** February 2026  
**Status:** Educational/Reference Implementation

## Overview

ShadowLink uses a **JSON-based HTTP protocol** for communication between the HQ Server and Field Agents. All endpoints follow RESTful conventions and use standard HTTP status codes.

## Protocol Basics

### Headers (Optional but Recommended)

All requests should include:
```
Content-Type: application/json
X-Protocol-Version: 1.0
Authorization: Bearer {api_key}  (for authenticated endpoints)
```

### Response Format

All responses follow this standard structure:

**Success Response:**
```json
{
  "status": "success|error",
  "data": { /* response data */ },
  "timestamp": "2026-02-10T12:00:00Z",
  "version": "1.0"
}
```

**Error Response:**
```json
{
  "status": "error",
  "error": "Error message",
  "code": "ERROR_CODE",
  "timestamp": "2026-02-10T12:00:00Z"
}
```

## API Endpoints

### Agent Management

#### 1. Create Agent
Create a new agent with registration code and API key.

```http
POST /api/agents/create
Content-Type: application/json

{
  "agent_name": "target-host-01"
}
```

**Response (201):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_id": "target-host-01",
  "registration_code": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6",
  "api_key": "x9y8z7a6b5c4d3e2f1g0h9i8j7k6l5m4n3o2p1q0r9s8t7u6v5w4x3y2z1",
  "status": "created"
}
```

---

#### 2. Agent Login
Authenticate agent using registration code.

```http
POST /api/agents/login
Content-Type: application/json

{
  "code": "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6"
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "agent_id": "target-host-01",
  "api_key": "x9y8z7a6b5c4d3e2f1g0h9i8j7k6l5m4n3o2p1q0r9s8t7u6v5w4x3y2z1",
  "status": "logged_in"
}
```

---

#### 3. List Agents
Get all agents and their status.

```http
GET /api/agents
```

**Response (200):**
```json
{
  "agents": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "agent_id": "target-host-01",
      "status": "online",
      "last_heartbeat": "2026-02-10T12:05:30Z",
      "registered_at": "2026-02-10T12:00:00Z",
      "commands_count": 5,
      "intel_count": 12,
      "ip_address": "192.168.1.100",
      "system_info": {
        "platform": "Linux",
        "cpu_cores": 4,
        "memory_gb": 8,
        "timezone": "UTC"
      }
    }
  ]
}
```

---

#### 4. Delete Agent
Delete agent and all associated data (commands, intel, messages).

```http
DELETE /api/agents/{agent_id}
```

**Response (200):**
```json
{
  "status": "deleted",
  "agent_id": "target-host-01"
}
```

**Note:** This performs a cascade delete - all related data is removed.

---

### Registration & Heartbeat

#### 5. Register Agent
Agent registers with HQ and submits initial system info.

```http
POST /api/register
Content-Type: application/json

{
  "agent_id": "target-host-01",
  "api_key": "x9y8z7a6b5c4d3e2f1g0h9i8j7k6l5m4n3o2p1q0r9s8t7u6v5w4x3y2z1",
  "system_info": {
    "platform": "Linux",
    "userAgent": "Mozilla/5.0...",
    "hardwareConcurrency": 4,
    "deviceMemory": 8,
    "timezone": "UTC"
  }
}
```

**Response (201):**
```json
{
  "status": "registered",
  "agent_id": "target-host-01"
}
```

---

#### 6. Send Heartbeat
Agent sends periodic heartbeat to maintain online status.

```http
POST /api/heartbeat
Content-Type: application/json

{
  "agent_id": "target-host-01",
  "api_key": "x9y8z7a6b5c4d3e2f1g0h9i8j7k6l5m4n3o2p1q0r9s8t7u6v5w4x3y2z1",
  "system_info": {
    "platform": "Linux",
    "hardwareConcurrency": 4,
    "timezone": "UTC"
  }
}
```

**Response (200):**
```json
{
  "status": "ok"
}
```

---

#### 7. Agent Logout
Gracefully disconnect agent from HQ.

```http
POST /api/agents/logout
Content-Type: application/json

{
  "agent_id": "target-host-01",
  "api_key": "x9y8z7a6b5c4d3e2f1g0h9i8j7k6l5m4n3o2p1q0r9s8t7u6v5w4x3y2z1"
}
```

**Response (200):**
```json
{
  "status": "disconnected",
  "agent_id": "target-host-01"
}
```

---

### Commands

#### 8. Send Command
HQ sends command to agent.

```http
POST /api/commands
Content-Type: application/json

{
  "agent_id": "target-host-01",
  "command_type": "info",
  "payload": {
    "action": "gather_system_info"
  }
}
```

**Allowed Command Types:**
- `info` - Information gathering
- `file` - File transfer operations
- `screenshot` - Screenshot capture
- `exec` - Command execution (not actually executed in this demo)

**Response (201):**
```json
{
  "command_id": "cmd_a1b2c3d4",
  "status": "queued"
}
```

---

#### 9. Fetch Pending Commands
Agent retrieves its pending commands.

```http
GET /api/commands/{agent_id}
```

**Response (200):**
```json
{
  "commands": [
    {
      "command_id": "cmd_a1b2c3d4",
      "command_type": "info",
      "payload": {
        "action": "gather_system_info"
      },
      "created_at": "2026-02-10T12:01:00Z"
    }
  ]
}
```

---

#### 10. Submit Command Result
Agent reports execution result back to HQ.

```http
POST /api/commands/{command_id}/result
Content-Type: application/json

{
  "agent_id": "target-host-01",
  "result": {
    "status": "success",
    "output": "Command executed successfully",
    "timestamp": "2026-02-10T12:02:00Z"
  }
}
```

**Response (200):**
```json
{
  "status": "received"
}
```

---

### Intelligence

#### 11. Submit Intelligence Data
Agent sends gathered intelligence to HQ.

```http
POST /api/intel
Content-Type: application/json

{
  "agent_id": "target-host-01",
  "data_type": "system_info",
  "data": {
    "hostname": "target-machine",
    "os": "Linux",
    "kernel": "5.10.0"
  }
}
```

**Supported Data Types:**
- `system_info` - OS, hardware information
- `network_info` - Network configuration
- `processes` - Running processes
- `files` - File system information
- `file_upload` - User-uploaded files (handled separately)

**Response (201):**
```json
{
  "status": "received", 
  "intel_id": "intel_xyz789"
}
```

---

#### 12. Retrieve Intelligence
HQ retrieves all intelligence from specific agent.

```http
GET /api/intel/{agent_id}
```

**Response (200):**
```json
{
  "intelligence": [
    {
      "id": "intel_xyz789",
      "data_type": "system_info",
      "data": {
        "hostname": "target-machine",
        "os": "Linux"
      },
      "created_at": "2026-02-10T12:01:30Z"
    }
  ]
}
```

---

### File Operations

#### 13. Upload File
Agent uploads file to HQ.

```http
POST /api/upload-file
Content-Type: multipart/form-data

Parameters:
- agent_id: (required) Agent identifier
- api_key: (required) Agent API key
- file: (required) File to upload
```

**Response (201):**
```json
{
  "status": "uploaded",
  "filename": "target-host-01_20260210_120130_document.txt",
  "original_name": "document.txt",
  "size": 2048
}
```

**File Storage:**
- Files stored in: `hq_server/uploads/`
- Naming format: `{agent_id}_{timestamp}_{original_filename}`
- Timestamp format: `YYYYMMDD_HHMMSS`

---

#### 14. Download File
HQ downloads file uploaded by agent.

```http
GET /api/download-file/{filename}
```

**Parameters:**
- `filename` - The file storage name (URL-encoded)

**Response (200):**
```
[File Binary Content]

Headers:
Content-Disposition: attachment; filename="document.txt"
Content-Type: application/octet-stream
```

**Example:**
```javascript
// Frontend code to download
const filename = encodeURIComponent('target-host-01_20260210_120130_document.txt');
window.location.href = `/api/download-file/${filename}`;
```

---

### Messages

#### 15. Send/Receive Message
Exchange messages between HQ and agent.

```http
POST /api/messages
Content-Type: application/json

{
  "agent_id": "target-host-01",
  "direction": "to_agent",  // or "from_agent"
  "message_type": "notification",
  "content": "Custom message content"
}
```

**Response (201):**
```json
{
  "status": "received",
  "message_id": "msg_abc123"
}
```

---

## Status Codes

| Code | Meaning | Description |
|------|---------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created |
| 400 | Bad Request | Invalid request parameters |
| 401 | Unauthorized | Invalid credentials or missing API key |
| 404 | Not Found | Agent or resource not found |
| 500 | Server Error | Internal server error |

---

## Error Codes

| Code | HTTP Status | Meaning |
|------|-------------|---------|
| AGENT_NOT_FOUND | 404 | Agent doesn't exist |
| INVALID_CREDENTIALS | 401 | Wrong API key or registration code |
| INVALID_COMMAND | 400 | Unknown command type |
| MISSING_PARAMETER | 400 | Required parameter missing |
| FILE_NOT_FOUND | 404 | Uploaded file not found |
| INVALID_FILE_PATH | 400 | Attempted directory traversal |
| INTERNAL_ERROR | 500 | Server-side error |

---

## Agent Status

- **offline** - Agent has not connected or has disconnected
- **online** - Agent is actively connected and sending heartbeats
- **executing** - Agent is executing a command (not actively used in v1.0)

---

## Heartbeat Specifications

**Heartbeat Interval:** 5 seconds (configurable)

**Timeout Rules:**
- If HQ doesn't receive heartbeat for >60 seconds, agent marked offline
- Agent should be prepared for failed heartbeats (network errors)
- Agents should reconnect gracefully after failures

---

## Authentication

Currently uses **Bearer Token** (API Key) authentication:

```
Authorization: Bearer {api_key}
```

Upgrade path for production:
- Implement TLS/SSL encryption
- Use certificate-based mutual authentication
- Add OAuth2 or JWT token support
- Implement token rotation/expiration

---

## Rate Limiting

Not implemented in v1.0. Production deployment should include:
- Requests per second per agent
- File upload size limits
- Command queue limits
- Intelligence data size limits

Suggested limits:
- 10 requests/second per agent
- 100MB max file upload
- 1000 pending commands max
- 10MB max intelligence data per submission

---

## Security Notes

⚠️ **This is an educational reference implementation. It is NOT production-ready.**

Missing in current version:
- ❌ TLS/SSL encryption
- ❌ Mutual authentication
- ❌ Input validation hardening
- ❌ Rate limiting and DDoS protection
- ❌ Command sandboxing
- ❌ Audit logging of sensitive operations

See ETHICAL_USE.md for full disclaimer.
