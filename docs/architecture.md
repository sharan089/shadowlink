# ShadowLink Architecture Documentation

**Version:** 1.0  
**Date:** February 2026  
**Type:** Educational Reference Implementation

## System Overview

ShadowLink demonstrates a **distributed agent-based command & control architecture** with the following design goals:

1. **Separation of Concerns** - Clear boundaries between networking, storage, and business logic
2. **Scalability** - Support multiple agents connecting to a central hub
3. **Auditability** - Log all operations for review
4. **Educational Clarity** - Simple enough to understand, complex enough to be realistic

```
┌──────────────────────────────────────────────────────────┐
│                    Field Agents (n)                       │
│                                                           │
│  ┌─────────────────┐    ┌─────────────────┐              │
│  │  Agent UI Loop  │    │  Agent UI Loop  │  ...          │
│  │ - Heartbeat     │    │ - Heartbeat     │              │
│  │ - Commands      │    │ - Commands      │              │
│  │ - Intel         │    │ - Intel         │              │
│  │ - Files         │    │ - Files         │              │
│  └────────┬────────┘    └────────┬────────┘              │
│           │ HTTPS                │ HTTPS                 │
└───────────┼────────────────────────┼────────────────────┘
            │                        │
            └───────────┬────────────┘
                        │
                        │ RESTful API
                        ▼
        ┌───────────────────────────────────┐
        │       HQ Server (Flask)            │
        ├───────────────────────────────────┤
        │  API Layer                        │
        │  ├─ /api/agents/*                │
        │  ├─ /api/commands/*              │
        │  ├─ /api/intel/*                 │
        │  ├─ /api/heartbeat               │
        │  └─ /api/upload-file             │
        ├───────────────────────────────────┤
        │  Business Logic                   │
        │  ├─ Agent Manager                │
        │  ├─ Command Queue                │
        │  ├─ Intel Processor              │
        │  └─ File Handler                 │
        ├───────────────────────────────────┤
        │  Data Layer                       │
        │  ├─ Agent Model                  │
        │  ├─ Command Model                │
        │  ├─ Intelligence Model           │
        │  └─ Message Model                │
        ├───────────────────────────────────┤
        │  Storage                          │
        │  ├─ SQLite Database              │
        │  └─ File System (/uploads/)      │
        └───────────────────────────────────┘
```

---

## Component Architecture

### 1. HQ Server (Central Hub)

**Files:**
- `main.py` - Flask application entry point
- `database.py` - SQLAlchemy ORM models
- `config.py` - Configuration settings

**Key Classes:**
- `Agent` - Represents connected agents
- `Command` - Represents pending commands
- `Intelligence` - Represents collected data
- `Message` - Represents inter-system messages

**Responsibilities:**
- Accept agent connections and heartbeats
- Queue commands for agents
- Receive and store intelligence data
- Manage file uploads/downloads
- Track agent status and metadata

**API Routes:** See `docs/protocol_specification.md`

---

## Data Flow Examples

### Example 1: Agent Registration & Heartbeat

```
Timeline:

1. HQ Creates Agent
   HQ Dashboard → POST /api/agents/create
   └─ DB: Insert Agent record (status: offline)

2. Agent Logs In
   Agent UI → POST /api/agents/login
   └─ Response: agent_id, api_key

3. Agent Registers with HQ
   Agent UI → POST /api/register
   ├─ system_info: {platform, CPU, memory, timezone}
   └─ DB: Update Agent status: online

4. Agent Sends Heartbeat (every 5s)
   Agent UI → POST /api/heartbeat
   └─ DB: Update Agent.last_heartbeat

5. HQ Detects Offline (60s+ without heartbeat)
   └─ Mark Agent.status: offline
```

### Example 2: Command Execution Flow

```
Timeline:

1. HQ Sends Command
   HQ Dashboard → POST /api/commands
   └─ DB: Insert Command (status: pending)

2. Agent Fetches Commands
   Agent UI → GET /api/commands/{agent_id}
   └─ Response: [pending commands]

3. Agent Executes & Reports
   Agent UI → Simulate execution
   └─ POST /api/commands/{id}/result

4. HQ Views Result
   HQ Dashboard → Shows status update
```

### Example 3: File Upload & Download

```
Timeline:

1. Agent Uploads File
   Agent UI → POST /api/upload-file
   ├─ File System: Save as {agent_id}_{timestamp}_{filename}
   ├─ DB: Create Intelligence record
   └─ Return: filename, size

2. HQ Downloads File
   HQ Dashboard → GET /api/download-file/{filename}
   ├─ Security: Verify path within /uploads/
   └─ Browser: Download file
```

---

## Database Schema

**Agents Table**
```
- id (PK)
- agent_id (UNIQUE)
- registration_code (UNIQUE)
- api_key (UNIQUE)
- status (online/offline)
- agent_metadata (JSON: ip_address, system_info, last_location)
- last_heartbeat
- registered_at
```

**Commands Table**
```
- id (PK)
- command_id (UNIQUE)
- agent_id (FK)
- command_type (exec, info, file, screenshot)
- payload (JSON)
- status (pending/executing/completed/failed)
- result (JSON, nullable)
- created_at
- executed_at
```

**Intelligence Table**
```
- id (PK)
- agent_id (FK)
- data_type (system_info, network_info, file_upload, etc)
- data (JSON)
- file_path (VARCHAR, for file uploads)
- created_at
```

**Relationships:**
- Agent → Commands (1:N, CASCADE delete)
- Agent → Intelligence (1:N, CASCADE delete)
- Agent → Messages (1:N, CASCADE delete)

---

## Security Posture

### Current Implementation
✅ API key authentication  
✅ Registration code (one-time use)  
✅ Command type whitelisting  
✅ File path validation  

### Missing (Production)
❌ TLS/SSL encryption  
❌ Mutual authentication  
❌ Audit logging  
❌ Rate limiting  
❌ Input validation (advanced)  
❌ Multi-user access control  

**See ETHICAL_USE.md for complete disclaimer.**

---

## Extension Points

### Add New Command Types
```python
# In HQ Dashboard UI, add option
<option value="new_type">New Type</option>

# In Agent UI, handle new type
if commandType === 'new_type':
  // Custom handling
```

### Add New Intelligence Types
```python
# Database supports arbitrary types
intelligence = Intelligence(
  agent_id=agent.id,
  data_type='new_intelligence_type',
  data={...}
)
```

### Add Encryption
```python
# Encrypt payloads in transit
payload = encrypt(commands, agent_public_key)
response = decrypt(payload, local_private_key)
```

---

## References

- **Protocol Spec:** `docs/protocol_specification.md`
- **Threat Model:** `docs/threat_model.md`
- **Ethical Use:** `ETHICAL_USE.md`
