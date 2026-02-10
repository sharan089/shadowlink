⚠️ **[IMPORTANT] This is a fictional, educational project. See [ETHICAL_USE.md](ETHICAL_USE.md) before using.**

# ShadowLink - Educational C2 Architecture Reference

A distributed command & control system designed to **teach distributed systems architecture, agent-based communication patterns, and API design**. This is a fully functional reference implementation suitable for learning and educational purposes.

## Overview

ShadowLink demonstrates how distributed agent systems communicate with a central command hub. It teaches educational concepts like:

- **Agent-Based Architecture** - Multiple independent agents connecting to central server
- **RESTful API Design** - Proper endpoint organization, status codes, error handling
- **Database Modeling** - Relationships, cascade operations, JSON fields
- **Real-time Synchronization** - Heartbeat patterns, status polling, command queueing
- **File Transfer** - Multipart uploads, secure download mechanisms
- **Full-Stack Development** - Backend (Flask + SQLAlchemy), Frontend (HTML/CSS/JS)

## ⚠️ Educational Use Only

**This code is intended for:**
- ✅ Learning distributed systems architecture
- ✅ Understanding agent-based communication
- ✅ Teaching API design principles
- ✅ Reference for security research
- ✅ Educational demonstrations in authorized settings

**This code is NOT intended for:**
- ❌ Unauthorized system access
- ❌ Actual command execution on systems you don't own
- ❌ Data exfiltration or theft
- ❌ Any form of actual malicious use

**Unauthorized computer access is illegal.** Using this code or derived principles for unauthorized access violates computer fraud laws. See [ETHICAL_USE.md](ETHICAL_USE.md) for complete disclaimer.

## Quick Start

### Prerequisites
- Python 3.13+
- pip
- Modern web browser
- Local machine only (not accessible from external networks)

### HQ Server

```bash
cd hq_server
pip install -r requirements.txt
python main.py

# Server runs on http://localhost:5000
# HQ Dashboard: http://localhost:5000
```

### Field Agent (Web-based)

```bash
# In separate browser tab/window
# http://localhost:5000/agent-ui

# You'll need a registration code from the HQ Dashboard
```

## Project Structure

```
shadowlink/
├── hq_server/                 # Central Flask server
│   ├── main.py                # API endpoints and Flask app
│   ├── database.py            # SQLAlchemy models
│   ├── config.py              # Server configuration
│   ├── templates/             
│   │   ├── hq_dashboard.html  # Command center UI
│   │   └── agent_ui.html      # Field agent web UI
│   ├── uploads/               # Uploaded files from agents
│   ├── requirements.txt        # Python dependencies
│   └── utils/
│       └── logger.py          # Logging utilities
├── docs/
│   ├── ARCHITECTURE.md        # Complete system design
│   ├── protocol_specification.md  # Detailed API spec
│   ├── architecture.md        # Component breakdown
│   ├── protocol.md            # Protocol definitions
│   └── threat_model.md        # Security considerations
├── shared/                    # Shared protocol definitions
│   ├── protocol.py
│   ├── constants.py
│   └── errors.py
├── ETHICAL_USE.md             # Legal and ethical guidance
├── README.md                  # This file
└── LICENSE                    # MIT License
```

## Features

### HQ Dashboard  
**Location:** `http://localhost:5000`

**Agent Management:**
- ✅ Create new agents (automatic registration code generation)
- ✅ View all agents with real-time status (online/offline)
- ✅ Display IP addresses and system information
- ✅ Monitor heartbeat status and last connection time
- ✅ Delete agents with cascade cleanup of all data

**Command Control:**
- ✅ Send commands to agents (types: exec, info, file, screenshot)
- ✅ Queue commands with custom payloads
- ✅ View command execution history
- ✅ Monitor command status (pending/completed/failed)

**Intelligence Collection:**
- ✅ Receive and display system information from agents
- ✅ Filter intelligence by agent and data type
- ✅ Download files uploaded by agents
- ✅ View collected data in structured format
- ✅ File management with timestamps and original names

**Real-time Updates:**
- ✅ Auto-refresh display every 1 second
- ✅ Live status indicators for agent connectivity
- ✅ Information persistence via SQLite database

### Field Agent UI  
**Location:** `http://localhost:5000/agent-ui`

**Connection Management:**
- ✅ Login with registration code from HQ
- ✅ Automatic system information capture (platform, CPU, memory, timezone)
- ✅ Periodic heartbeat sends (every 5 seconds)
- ✅ Auto-disconnect on page close with immediate server notification

**Command Execution:**
- ✅ View incoming commands from HQ
- ✅ Execute commands (simulated - no actual commands run)
- ✅ Report execution results back to HQ
- ✅ Command status logging with timestamps

**Intelligence & Files:**
- ✅ Drag-and-drop file upload interface
- ✅ Submit system intelligence data to HQ
- ✅ View upload status and confirmation messages
- ✅ Automatic download link generation for HQ access

**Real-time Communication:**
- ✅ Polling mechanism for commands every 3 seconds
- ✅ Automatic heartbeat every 5 seconds
- ✅ Immediate disconnect notification to HQ

## Technical Architecture

### Backend Stack
- **Framework:** Flask 2.3.0 (lightweight, educational)
- **ORM:** SQLAlchemy 3.0.5 with Flask-SQLAlchemy
- **Database:** SQLite (file-based, zero configuration)
- **Python:** 3.13+
- **HTTP:** RESTful with JSON payloads

### Frontend Stack
- **Languages:** HTML5, CSS3, Vanilla JavaScript (no frameworks)
- **Style:** Dark theme inspired by GitHub
- **API Client:** Fetch API (native browser, no external dependencies)
- **Updates:** Polling-based synchronization (every 1-3 seconds)

### Communication Protocol
- **Transport:** HTTP/REST (educational - not encrypted)
- **Data Format:** JSON
- **Authentication:** API Key (bearer token) + Registration Code (one-time use)
- **Error Handling:** Standard HTTP status codes with descriptive messages

See [docs/protocol_specification.md](docs/protocol_specification.md) for complete API reference.

## Database Design

### Agent Model
```
agent_id          - Unique identifier for agent
registration_code - One-time use code for initial login
api_key           - Persistent bearer token for authentication
status            - Current state: online/offline
agent_metadata    - JSON field storing:
                    • ip_address: Remote agent IP
                    • system_info: {platform, CPU, memory, timezone}
                    • last_location: IP and timestamp
last_heartbeat    - Timestamp of last connection
registered_at     - When agent was created
```

**Relationships:**
- Agents → Commands (1:N relationship, CASCADE delete)
- Agents → Intelligence (1:N relationship, CASCADE delete)
- Agents → Messages (1:N relationship, CASCADE delete)

### File Storage
- **Location:** `hq_server/uploads/`
- **Naming:** `{agent_id}_{YYYYMMDD_HHMMSS}_{original_filename}`
- **Access:** `/api/download-file/{filename}` with URL encoding
- **Security:** Path validation prevents directory traversal attacks

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for complete database schema.

## API Endpoints

### Agent Management
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/agents/create` | Create new agent with registration code |
| POST | `/api/agents/login` | Agent login with code |
| GET | `/api/agents` | List all agents with status |
| DELETE | `/api/agents/{id}` | Delete agent (cascade deletes all data) |

### Commands & Control
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/commands` | Send command to agent |
| GET | `/api/commands/{agent_id}` | Fetch pending commands |
| POST | `/api/commands/{id}/result` | Report command result |

### Intelligence & Data
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/intel` | Submit intelligence data |
| GET | `/api/intel/{agent_id}` | Get agent intelligence |
| POST | `/api/upload-file` | Upload file (multipart) |
| GET | `/api/download-file/{name}` | Download file |

### Heartbeat & Status
| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/register` | Register with system info |
| POST | `/api/heartbeat` | Send heartbeat (keep alive) |
| POST | `/api/agents/logout` | Graceful disconnect |

See [docs/protocol_specification.md](docs/protocol_specification.md) for detailed specifications including payloads and responses.

## Configuration

### HQ Server
Edit `hq_server/config.py`:
```python
HQ_HOST = "0.0.0.0"              # Bind address (all interfaces)
HQ_PORT = 5000                   # Listen port
DEBUG = True                     # Debug mode flag
HEARTBEAT_TIMEOUT = 60           # Agent offline threshold (seconds)
HEARTBEAT_INTERVAL = 30          # Expected heartbeat frequency
```

### Agent
Edit `agent/config.py`:
```python
HQ_URL = "http://localhost:5000" # HQ server URL
AGENT_ID = "agent_001"           # Agent identifier  
HEARTBEAT_INTERVAL = 30          # Heartbeat frequency (seconds)
```

## Workflow Examples

### 1. Create and Connect an Agent

```
Step 1: HQ Dashboard → Create Agent Panel
   - Enter name: "target-host-01"
   - Click "Create Agent"
   - Receive registration code and API key

Step 2: Agent UI → Login
   - Navigate to http://localhost:5000/agent-ui
   - Paste registration code
   - Click "Connect to HQ"
   
Step 3: Automatic Registration
   - Agent automatically captures system info
   - Sends heartbeat to confirm connection
   - Agent appears "ONLINE" in HQ Dashboard

Step 4: Continuous Synchronization
   - Agent sends heartbeat every 5 seconds
   - HQ updates status every 1 second
   - Agent marked offline after 60 seconds without heartbeat
```

### 2. Send Command and Get Result

```
Step 1: HQ Dashboard → Commands Tab
   - Select agent from dropdown
   - Choose command type (exec, info, file, screenshot)
   - Enter payload/details
   - Click "Send Command"

Step 2: Agent UI → Receive & Execute
   - Command appears in "Received Commands" panel
   - Click command to select it
   - Click "Execute Selected" button
   - Simulated execution completes

Step 3: Result Submission
   - Execution result automatically sent to HQ
   - Status changes to "completed"
   - Result displayed in command panel

Step 4: HQ Views Result
   - HQ Dashboard updates automatically
   - Command shows in history with result
   - Operator can review execution details
```

### 3. Upload File from Agent

```
Step 1: Agent UI → File Upload
   - Drag file into "Drop Zone" or click to select
   - File begins uploading
   - Progress indicator shows upload status

Step 2: Server Processing
   - File saved to hq_server/uploads/
   - Named: target-host-01_20260210_120130_document.txt
   - Intelligence record created in database

Step 3: HQ Dashboard → Intelligence Tab
   - File appears in collected intelligence
   - Shows file name, size, and storage ID
   - Download link automatically generated

Step 4: HQ Downloads
   - Click download link
   - Browser saves file with original name
   - File transfer complete
```

## Security Architecture

### Current Security (Educational Implementation)
- ✅ **API Key Authentication** - Bearer token authentication
- ✅ **Registration Code** - One-time use for initial login
- ✅ **Command Type Whitelisting** - Only specific commands allowed
- ✅ **File Path Validation** - Prevents directory traversal attacks
- ✅ **Input Validation** - Basic validation of parameters
- ✅ **Error Handling** - Proper error messages without information leakage
- ✅ **Cascade Operations** - Ensure data integrity on deletion

### Missing for Production Use
- ❌ **TLS/SSL Encryption** - All traffic is plaintext HTTP
- ❌ **Mutual Authentication** - No certificate validation
- ❌ **Rate Limiting** - No DDoS or brute force protection
- ❌ **Audit Logging** - Operations not fully logged
- ❌ **Advanced Validation** - Limited input sanitization
- ❌ **Multi-user** - Single access, no per-user isolation
- ❌ **Session Management** - No session expiration
- ❌ **CSRF Protection** - No CSRF tokens

**This is NOT production-grade code.** See [ETHICAL_USE.md](ETHICAL_USE.md) for complete security limitations and threat model.

## Learning Outcomes

By studying and using ShadowLink, you'll understand:

### System Architecture
- ✅ Distributed agent-server communication patterns
- ✅ Heartbeat mechanisms for status monitoring
- ✅ Command queueing and delivery systems
- ✅ Real-time data synchronization techniques
- ✅ Database relationship modeling

### Web Development
- ✅ RESTful API design principles
- ✅ Frontend state management in JavaScript
- ✅ Form handling and file uploads
- ✅ Real-time UI updates via polling
- ✅ DOM manipulation and event handling

### Database Design
- ✅ Relationship modeling (1:N, N:M patterns)
- ✅ Cascade operations and referential integrity
- ✅ JSON fields for semi-structured data
- ✅ Query optimization and indexing
- ✅ SQLAlchemy ORM usage

### Security (Defensive Awareness)
- ✅ How to identify security vulnerabilities
- ✅ Input validation and output encoding techniques
- ✅ API authentication mechanisms
- ✅ Path traversal attack prevention
- ✅ Threat modeling and risk assessment
- ✅ Encryption and secure communication needs

## Documentation

- **[Full Architecture](docs/ARCHITECTURE.md)** - System design, components, data flow, scalability
- **[Protocol Specification](docs/protocol_specification.md)** - Complete API reference with examples
- **[Architecture Overview](docs/architecture.md)** - Component breakdown and relationships
- **[Threat Model](docs/threat_model.md)** - Security considerations and future enhancements
- **[Ethical Use](ETHICAL_USE.md)** - Legal and ethical guidelines
- **[License](LICENSE)** - MIT License

## Troubleshooting

### Server Won't Start

```bash
# Check Python version (need 3.13+)
python --version

# Clear old database file
rm hq_server/shadowlink.db

# Install/update dependencies
pip install -r hq_server/requirements.txt --upgrade

# Run with verbose output
python hq_server/main.py
```

### Agent Won't Connect

```bash
# Verify HQ server is running
curl http://localhost:5000/

# Check browser console (F12 → Console tab)
# for JavaScript errors

# Verify registration code:
# - Copy code exactly from HQ Dashboard
# - Paste into Agent UI
# - Check for typos
```

### Can't Download Files

```bash
# Verify files exist
ls hq_server/uploads/

# Check browser console for errors
# F12 → Console tab → Look for failed requests

# Verify URL encoding in download link
# Filename should be: agent_id_timestamp_filename.ext
```

## Deployment

Ready to take ShadowLink public? We've made it easy with guides for both platforms:

### Option 1: PythonAnywhere (Recommended)
Deploy your Flask backend to PythonAnywhere for free:
- Automatic Flask support
- SQLite included
- HTTPS enabled
- Perfect for educational projects

**Setup Time:** ~15-20 minutes  
**See:** [PYTHONANYWHERE_DEPLOYMENT.md](docs/PYTHONANYWHERE_DEPLOYMENT.md)

### Option 2: GitHub Pages + PythonAnywhere (Best Practice)
Hybrid deployment for maximum flexibility:
- Backend API on PythonAnywhere
- Documentation site on GitHub Pages
- Completely free tier available
- Professional separation of concerns

**Setup Time:** ~40 minutes  
**See:** [GITHUB_PAGES_DEPLOYMENT.md](docs/GITHUB_PAGES_DEPLOYMENT.md)

### Quick Deployment Checklist
- [ ] Create `requirements.txt` (provided)
- [ ] Create PythonAnywhere account
- [ ] Clone repository to PythonAnywhere
- [ ] Configure WSGI application
- [ ] Initialize database on server
- [ ] Test API endpoints
- [ ] Update frontend API URLs

**Full Guide:** [DEPLOYMENT_SUMMARY.md](docs/DEPLOYMENT_SUMMARY.md)

## Interview Discussion Points

This project demonstrates:

### Full-Stack Development
- "I built both backend (Flask) and frontend (vanilla JS) from scratch"
- "I implemented database layer using SQLAlchemy ORM"
- "The project uses no external JavaScript frameworks"

### System Design & Architecture
- "I designed a distributed agent-based system"
- "I modeled agent-command relationships with cascade deletion"
- "I used JSON fields for flexible metadata storage"
- "I implemented heartbeat monitoring for real-time status"

### API & REST Design
- "I designed RESTful endpoints following HTTP conventions"
- "I implemented proper error handling and status codes"
- "I documented the complete API specification"
- "I secured endpoints with API key authentication"

### Real-time Synchronization
- "I implemented polling-based real-time updates"
- "I handled disconnection detection with heartbeat timeout"
- "I designed auto-reconnection mechanisms"

### Security Mindset
- "I validated file paths to prevent directory traversal"
- "I implemented API key authentication with unique tokens"
- "I command type whitelisting for safety"
- "I documented security limitations and threat model"
- "I created educational disclaimers for responsible use"

### Code Quality
- "I separated concerns between API, business logic, and data layers"
- "I used proper database relationships and constraints"
- "I implemented comprehensive error handling"
- "I documented code extensively for clarity"

## Future Enhancements

Potential improvements for advanced learners:

- [ ] **Encryption** - Implement TLS/SSL with certificate validation
- [ ] **Advanced Auth** - OAuth2 or JWT token-based authentication
- [ ] **WebSocket** - Replace polling with real-time push via WebSocket
- [ ] **Message Encryption** - End-to-end encryption with RSA/AES
- [ ] **Scalability** - Distribute database (PostgreSQL) and file storage (S3)
- [ ] **Multi-user** - Role-based access control (RBAC)
- [ ] **Audit Logging** - Comprehensive logging of all operations
- [ ] **Rate Limiting** - Prevent DoS attacks and brute force
- [ ] **Job Queue** - Async task processing with Celery
- [ ] **Monitoring** - Prometheus metrics and Grafana dashboards

## Resources for Learning

### Web Development
- **Flask Documentation:** https://flask.palletsprojects.com/
- **SQLAlchemy ORM:** https://www.sqlalchemy.org/
- **JavaScript Fetch API:** https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API

### API Design
- **RESTful API Design:** https://restfulapi.net/
- **HTTP Status Codes:** https://httpwg.org/specs/rfc7231.html#status.codes
- **JSON Schema:** https://json-schema.org/

### Security
- **OWASP Top 10:** https://owasp.org/www-project-top-ten/
- **Web Security Academy:** https://portswigger.net/web-security
- **API Security:** https://owasp.org/www-project-api-security/

## License

MIT License - See [LICENSE](LICENSE) file for details.

## Contributing

This is an educational reference project. Improvements welcome:

1. Maintain educational clarity
2. Add comprehensive documentation
3. Follow security best practices
4. Update threat model for changes
5. Include code examples and explanations

---

**⚠️ IMPORTANT: Unauthorized computer access is illegal. This project is for learning only. See [ETHICAL_USE.md](ETHICAL_USE.md).**

**Last Updated:** February 2026
#   s h a d o w l i n k  
 