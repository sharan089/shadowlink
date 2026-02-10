# GitHub Pages Deployment Guide

Deploy ShadowLink documentation and a landing page to GitHub Pages while running the Flask backend on PythonAnywhere.

## How GitHub Pages Fits In

**GitHub Pages** = Static documentation + landing page  
**PythonAnywhere** = Flask backend + API + Web UIs

This two-tier approach:
- Documentation hosted free on GitHub Pages
- Backend API running on PythonAnywhere
- Frontend UIs call the PythonAnywhere API

## Step 1: Create GitHub Pages Branch

In your repository:

```bash
git checkout --orphan gh-pages
git rm -rf .
```

## Step 2: Create Documentation Structure

Create this directory structure in the `gh-pages` branch:

```
/
├── index.html              (Landing page)
├── css/
│   └── style.css
├── docs/
│   ├── api.html            (API Endpoints)
│   ├── architecture.html    (System Design)
│   ├── deployment.html      (Both deployment guides)
│   └── ethical.html         (Ethical use notice)
└── dashboard-link.html      (Link to PythonAnywhere backend)
```

## Step 3: Create Landing Page (index.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ShadowLink - Command & Control System</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>ShadowLink</h1>
            <ul class="nav-links">
                <li><a href="#overview">Overview</a></li>
                <li><a href="#docs">Documentation</a></li>
                <li><a href="#dashboard">Dashboard</a></li>
                <li><a href="#api">API</a></li>
            </ul>
        </div>
    </nav>

    <header class="hero">
        <div class="container">
            <h1>ShadowLink C2 System</h1>
            <p>Distributed Command & Control Framework</p>
            <div class="buttons">
                <a href="#dashboard" class="btn btn-primary">Access Dashboard</a>
                <a href="docs/api.html" class="btn btn-secondary">View API Docs</a>
            </div>
        </div>
    </header>

    <section id="overview" class="overview">
        <div class="container">
            <h2>System Overview</h2>
            <div class="features">
                <div class="feature">
                    <h3>🎯 Agent Management</h3>
                    <p>Create, monitor, and control distributed agents across networks</p>
                </div>
                <div class="feature">
                    <h3>📊 Intelligence Collection</h3>
                    <p>Real-time system information, file uploads, and data gathering</p>
                </div>
                <div class="feature">
                    <h3>⚡ Command Execution</h3>
                    <p>Queue and execute commands on agents with result reporting</p>
                </div>
                <div class="feature">
                    <h3>🔐 Secure Communication</h3>
                    <p>API key authentication, registration codes, and encrypted metadata</p>
                </div>
            </div>
        </div>
    </section>

    <section id="docs" class="documentation">
        <div class="container">
            <h2>Documentation</h2>
            <ul class="doc-links">
                <li><a href="docs/api.html">API Specification v1.0</a> - Complete endpoint reference</li>
                <li><a href="docs/architecture.html">Architecture & Design</a> - System components and flows</li>
                <li><a href="docs/deployment.html">Deployment Guides</a> - PythonAnywhere & GitHub Pages</li>
                <li><a href="docs/ethical.html">Ethical Use & Legal</a> - CFAA compliance and warnings</li>
            </ul>
        </div>
    </section>

    <section id="dashboard" class="dashboard-section">
        <div class="container">
            <h2>Access Dashboard</h2>
            <p>Connect to the deployed backend to access the HQ command center:</p>
            <div class="dashboard-info">
                <h3>Backend Status</h3>
                <p id="backend-status">Checking connection...</p>
                <a href="" id="dashboard-link" class="btn btn-primary" style="display:none;">
                    Open HQ Dashboard →
                </a>
            </div>
        </div>
    </section>

    <section id="api" class="api-section">
        <div class="container">
            <h2>API Quick Reference</h2>
            <div class="endpoints">
                <div class="endpoint">
                    <code>POST /api/agents/create</code>
                    <p>Create new agent with registration code</p>
                </div>
                <div class="endpoint">
                    <code>POST /api/agents/login</code>
                    <p>Agent login with registration code</p>
                </div>
                <div class="endpoint">
                    <code>GET /api/agents</code>
                    <p>List all agents with status</p>
                </div>
                <div class="endpoint">
                    <code>POST /api/heartbeat</code>
                    <p>Agent heartbeat with system info</p>
                </div>
                <div class="endpoint">
                    <code>POST /api/commands</code>
                    <p>Send command to agent</p>
                </div>
            </div>
            <p><a href="docs/api.html">View Complete API Documentation →</a></p>
        </div>
    </section>

    <footer>
        <div class="container">
            <p>&copy; 2026 ShadowLink | Educational & Authorized Use Only</p>
            <p><a href="docs/ethical.html">Ethical Use Notice</a> | <a href="docs/api.html">API Docs</a></p>
        </div>
    </footer>

    <script>
        // Check backend connectivity
        async function checkBackend() {
            const backendUrl = 'https://{YOUR_PYTHONANYWHERE_USERNAME}.pythonanywhere.com';
            const statusEl = document.getElementById('backend-status');
            const linkEl = document.getElementById('dashboard-link');
            
            try {
                const response = await fetch(backendUrl + '/api/agents');
                if (response.ok) {
                    statusEl.textContent = '✅ Backend is online and running';
                    statusEl.style.color = '#4ade80';
                    linkEl.href = backendUrl;
                    linkEl.style.display = 'inline-block';
                } else {
                    throw new Error('Backend responded with error');
                }
            } catch (error) {
                statusEl.textContent = '❌ Backend is offline or unreachable';
                statusEl.style.color = '#ef4444';
                linkEl.style.display = 'none';
            }
        }
        
        // Check backend on page load and every 30 seconds
        checkBackend();
        setInterval(checkBackend, 30000);
    </script>
</body>
</html>
```

## Step 4: Create CSS Styling (css/style.css)

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    line-height: 1.6;
    color: #333;
    background: #f9fafb;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
}

/* Navbar */
.navbar {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    color: white;
    padding: 1rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.navbar h1 {
    font-size: 1.5rem;
    margin-bottom: 0.5rem;
}

.navbar .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.nav-links {
    display: flex;
    list-style: none;
    gap: 2rem;
}

.nav-links a {
    color: #e2e8f0;
    text-decoration: none;
    transition: color 0.3s;
}

.nav-links a:hover {
    color: #60a5fa;
}

/* Hero Section */
.hero {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    color: white;
    padding: 6rem 0;
    text-align: center;
}

.hero h1 {
    font-size: 3rem;
    margin-bottom: 1rem;
    font-weight: 700;
}

.hero p {
    font-size: 1.25rem;
    margin-bottom: 2rem;
    opacity: 0.9;
}

.buttons {
    display: flex;
    gap: 1rem;
    justify-content: center;
    flex-wrap: wrap;
}

.btn {
    display: inline-block;
    padding: 0.75rem 1.5rem;
    border-radius: 0.5rem;
    text-decoration: none;
    font-weight: 600;
    transition: all 0.3s;
}

.btn-primary {
    background: #3b82f6;
    color: white;
}

.btn-primary:hover {
    background: #2563eb;
    transform: translateY(-2px);
}

.btn-secondary {
    background: transparent;
    color: white;
    border: 2px solid #60a5fa;
}

.btn-secondary:hover {
    background: #60a5fa;
    color: #0f172a;
}

/* Sections */
section {
    padding: 4rem 0;
}

section h2 {
    font-size: 2rem;
    margin-bottom: 2rem;
    text-align: center;
    color: #1e293b;
}

/* Features */
.features {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 2rem;
    margin-top: 3rem;
}

.feature {
    background: white;
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    transition: transform 0.3s;
}

.feature:hover {
    transform: translateY(-5px);
}

.feature h3 {
    margin-bottom: 1rem;
    color: #3b82f6;
}

/* Documentation Links */
.doc-links {
    list-style: none;
    display: grid;
    gap: 1rem;
    max-width: 600px;
    margin: 0 auto;
}

.doc-links a {
    display: block;
    padding: 1rem;
    background: white;
    border-left: 4px solid #3b82f6;
    text-decoration: none;
    color: #1e293b;
    transition: all 0.3s;
}

.doc-links a:hover {
    background: #f0f9ff;
    border-left-color: #2563eb;
}

/* Dashboard Info */
.dashboard-info {
    background: white;
    padding: 2rem;
    border-radius: 0.5rem;
    max-width: 500px;
    margin: 0 auto;
    text-align: center;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

#backend-status {
    font-weight: 600;
    margin: 1rem 0;
    font-size: 1.1rem;
}

/* API Section */
.endpoints {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5rem;
    margin: 2rem 0;
}

.endpoint {
    background: white;
    padding: 1.5rem;
    border-radius: 0.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border-left: 3px solid #10b981;
}

.endpoint code {
    background: #f3f4f6;
    padding: 0.25rem 0.5rem;
    border-radius: 0.25rem;
    font-family: 'Courier New', monospace;
    font-weight: 600;
    color: #7c3aed;
}

/* Footer */
footer {
    background: #1e293b;
    color: white;
    padding: 2rem 0;
    text-align: center;
    margin-top: 4rem;
}

footer a {
    color: #60a5fa;
    text-decoration: none;
}

footer a:hover {
    text-decoration: underline;
}

/* Responsive */
@media (max-width: 768px) {
    .hero h1 {
        font-size: 2rem;
    }
    
    .nav-links {
        gap: 1rem;
    }
    
    .buttons {
        flex-direction: column;
    }
    
    .btn {
        width: 100%;
        text-align: center;
    }
}
```

## Step 5: Create API Documentation Page (docs/api.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Specification v1.0 - ShadowLink</title>
    <link rel="stylesheet" href="../css/style.css">
    <style>
        .api-detail { background: white; padding: 2rem; margin: 1rem 0; border-radius: 0.5rem; }
        .method { color: #10b981; font-weight: 600; }
        .endpoint-url { background: #f3f4f6; padding: 0.5rem; border-radius: 0.25rem; font-family: monospace; }
        pre { background: #1e293b; color: #e2e8f0; padding: 1rem; border-radius: 0.5rem; overflow-x: auto; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>ShadowLink</h1>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="#agents">Agents</a></li>
                <li><a href="#commands">Commands</a></li>
                <li><a href="#intel">Intelligence</a></li>
            </ul>
        </div>
    </nav>

    <section style="padding: 2rem 0;">
        <div class="container">
            <h1>API Specification v1.0</h1>
            <p style="margin-top: 1rem; color: #666;">Complete reference for all ShadowLink API endpoints</p>

            <h2 id="agents">Agent Management</h2>

            <div class="api-detail">
                <h3><span class="method">POST</span> /api/agents/create</h3>
                <p>Create a new agent with registration code</p>
                <p><strong>Request:</strong></p>
                <pre>POST /api/agents/create
Content-Type: application/json

{
  "agent_name": "agent_alpha"
}</pre>
                <p><strong>Response (201):</strong></p>
                <pre>{
  "id": 1,
  "agent_id": "agent_alpha",
  "registration_code": "a1b2c3d4e5f6...",
  "api_key": "secret_key_...",
  "status": "created"
}</pre>
            </div>

            <div class="api-detail">
                <h3><span class="method">POST</span> /api/agents/login</h3>
                <p>Agent login with registration code</p>
                <p><strong>Request:</strong></p>
                <pre>POST /api/agents/login
Content-Type: application/json

{
  "code": "a1b2c3d4e5f6..."
}</pre>
                <p><strong>Response (200):</strong></p>
                <pre>{
  "id": 1,
  "agent_id": "agent_alpha",
  "api_key": "secret_key_...",
  "status": "logged_in"
}</pre>
            </div>

            <div class="api-detail">
                <h3><span class="method">GET</span> /api/agents</h3>
                <p>List all agents with status</p>
                <p><strong>Response (200):</strong></p>
                <pre>{
  "agents": [
    {
      "id": 1,
      "agent_id": "agent_alpha",
      "status": "online",
      "ip_address": "192.168.1.100",
      "commands_count": 5,
      "intel_count": 3
    }
  ]
}</pre>
            </div>

            <div class="api-detail">
                <h3><span class="method">DELETE</span> /api/agents/&lt;agent_id&gt;</h3>
                <p>Delete an agent and all associated data</p>
                <p><strong>Response (200):</strong></p>
                <pre>{
  "status": "deleted",
  "agent_id": "agent_alpha"
}</pre>
            </div>

            <h2 id="commands">Commands</h2>

            <div class="api-detail">
                <h3><span class="method">POST</span> /api/commands</h3>
                <p>Send command to agent</p>
                <p><strong>Request:</strong></p>
                <pre>POST /api/commands
Content-Type: application/json

{
  "agent_id": "agent_alpha",
  "command_type": "system_info",
  "payload": {}
}</pre>
                <p><strong>Response (201):</strong></p>
                <pre>{
  "command_id": "cmd_a1b2c3d4",
  "status": "queued"
}</pre>
            </div>

            <div class="api-detail">
                <h3><span class="method">GET</span> /api/commands/&lt;agent_id&gt;</h3>
                <p>Get pending commands for agent</p>
                <p><strong>Response (200):</strong></p>
                <pre>{
  "commands": [
    {
      "command_id": "cmd_a1b2c3d4",
      "command_type": "system_info",
      "payload": {}
    }
  ]
}</pre>
            </div>

            <h2 id="intel">Intelligence</h2>

            <div class="api-detail">
                <h3><span class="method">POST</span> /api/intel</h3>
                <p>Submit intelligence data from agent</p>
                <p><strong>Request:</strong></p>
                <pre>POST /api/intel
Content-Type: application/json

{
  "agent_id": "agent_alpha",
  "data_type": "system_info",
  "data": {
    "platform": "linux",
    "processor": "Intel i7",
    "memory": "16GB"
  }
}</pre>
                <p><strong>Response (201):</strong></p>
                <pre>{
  "status": "received",
  "intel_id": 1
}</pre>
            </div>

            <div class="api-detail">
                <h3><span class="method">GET</span> /api/intel/&lt;agent_id&gt;</h3>
                <p>Get intelligence from agent</p>
                <p><strong>Response (200):</strong></p>
                <pre>{
  "intelligence": [
    {
      "id": 1,
      "data_type": "system_info",
      "data": { "platform": "linux" }
    }
  ]
}</pre>
            </div>

            <div class="api-detail">
                <h3><span class="method">POST</span> /api/upload-file</h3>
                <p>Upload file from agent</p>
                <p><strong>Request:</strong></p>
                <pre>POST /api/upload-file
Content-Type: multipart/form-data

agent_id: agent_alpha
api_key: secret_key_...
file: [binary file data]</pre>
                <p><strong>Response (201):</strong></p>
                <pre>{
  "status": "uploaded",
  "filename": "agent_alpha_20260210_120000_config.txt",
  "original_name": "config.txt",
  "size": 1024
}</pre>
            </div>

            <p style="margin-top: 2rem; padding: 1rem; background: #fef0f0; border-radius: 0.5rem; border-left: 3px solid #ef4444;">
                <strong>⚠️ Legal Notice:</strong> This system is for authorized security research and penetration testing only. 
                Unauthorized access is prohibited by the CFAA. Review <a href="ethical.html">Ethical Use Guidelines</a>.
            </p>
        </div>
    </section>
</body>
</html>
```

## Step 6: Create Architecture Documentation (docs/architecture.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Architecture - ShadowLink</title>
    <link rel="stylesheet" href="../css/style.css">
    <style>
        .diagram { background: #f3f4f6; padding: 1rem; border-radius: 0.5rem; margin: 1rem 0; font-family: monospace; }
        .architecture-box { background: white; padding: 1.5rem; margin: 1rem 0; border-radius: 0.5rem; border-left: 4px solid #3b82f6; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>ShadowLink</h1>
            <ul class="nav-links">
                <li><a href="/">Home</a></li>
                <li><a href="#overview">Overview</a></li>
                <li><a href="#components">Components</a></li>
            </ul>
        </div>
    </nav>

    <section style="padding: 2rem 0;">
        <div class="container">
            <h1>System Architecture</h1>

            <h2 id="overview">System Overview</h2>

            <div class="architecture-box">
                <h3>Three-Tier Architecture</h3>
                <div class="diagram">
┌─────────────────────────────────────┐
│     GitHub Pages (Static)           │
│  - Landing page                     │
│  - Documentation                    │
│  - API Reference                    │
└──────────────┬──────────────────────┘
               │
               │ HTTP/HTTPS
               ▼
┌─────────────────────────────────────┐
│   PythonAnywhere (Flask Backend)    │
│  - HQ Dashboard UI                  │
│  - Agent UI                         │
│  - API Endpoints (20+)              │
│  - SQLite Database                  │
└──────────────┬──────────────────────┘
               │
         HTTP Polling
               │
         ┌─────┴─────┐
         ▼           ▼
    ┌─────────┐ ┌─────────┐
    │ Agent 1 │ │ Agent 2 │
    └─────────┘ └─────────┘
                </div>
            </div>

            <h2 id="components">Components</h2>

            <div class="architecture-box">
                <h3>1. HQ Dashboard (hq_dashboard.html)</h3>
                <ul>
                    <li><strong>Agents Tab:</strong> Create agents, view status, delete agents</li>
                    <li><strong>Commands Tab:</strong> Send commands to agents, view history</li>
                    <li><strong>Intelligence Tab:</strong> Collect data, filter, download files</li>
                    <li><strong>Real-time Updates:</strong> 1-second polling interval</li>
                </ul>
            </div>

            <div class="architecture-box">
                <h3>2. Agent UI (agent_ui.html)</h3>
                <ul>
                    <li><strong>Login:</strong> Registration code → API key</li>
                    <li><strong>System Capture:</strong> Platform, CPU, Memory, Timezone</li>
                    <li><strong>Heartbeat:</strong> 5-second intervals with system info</li>
                    <li><strong>Command Polling:</strong> 3-second check for pending commands</li>
                    <li><strong>File Operations:</strong> Drag-drop upload, download</li>
                    <li><strong>Auto-Disconnect:</strong> Graceful cleanup on page close</li>
                </ul>
            </div>

            <div class="architecture-box">
                <h3>3. Flask Backend (main.py)</h3>
                <ul>
                    <li><strong>20+ API Endpoints:</strong> Agent, Command, Intelligence, File operations</li>
                    <li><strong>Authentication:</strong> Registration codes + API keys</li>
                    <li><strong>Database:</strong> SQLite with SQLAlchemy ORM</li>
                    <li><strong>File Storage:</strong> Local uploads/ directory</li>
                </ul>
            </div>

            <div class="architecture-box">
                <h3>4. Database Schema</h3>
                <div class="diagram">
Agent
├── id (primary key)
├── agent_id (string)
├── registration_code
├── api_key
├── status (online/offline)
├── last_heartbeat
├── agent_metadata (JSON)
└── registered_at

Command
├── id (primary key)
├── command_id (string)
├── agent_id (FK)
├── command_type
├── payload (JSON)
├── result (JSON)
├── status (pending/completed)
└── created_at, executed_at

Intelligence
├── id (primary key)
├── agent_id (FK)
├── data_type
├── data (JSON)
├── file_path (for uploads)
└── created_at

Message
├── id (primary key)
├── agent_id (FK)
├── direction (to/from agent)
├── message_type
├── content
└── created_at
                </div>
            </div>

            <p style="margin-top: 2rem; padding: 1rem; background: #fef0f0; border-radius: 0.5rem; border-left: 3px solid #ef4444;">
                <strong>⚠️ Ethical Notice:</strong> This documentation is for educational purposes. Review <a href="ethical.html">Ethical Use Guidelines</a> before any operational use.
            </p>
        </div>
    </section>
</body>
</html>
```

## Step 7: Create Ethical Use Page (docs/ethical.html)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ethical Use & Legal - ShadowLink</title>
    <link rel="stylesheet" href="../css/style.css">
    <style>
        .warning { background: #fef0f0; border-left: 4px solid #ef4444; padding: 1rem; margin: 1rem 0; border-radius: 0.5rem; }
        .authorized { background: #f0fdf4; border-left: 4px solid #10b981; padding: 1rem; margin: 1rem 0; border-radius: 0.5rem; }
    </style>
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <h1>ShadowLink</h1>
        </div>
    </nav>

    <section style="padding: 2rem 0;">
        <div class="container">
            <h1>Ethical Use & Legal Compliance</h1>

            <div class="warning">
                <h2 style="margin-top: 0;">⚠️ COMPUTER FRAUD AND ABUSE ACT (CFAA) WARNING</h2>
                <p style="margin-bottom: 0;">
                    Unauthorized access to computers is a federal crime under the Computer Fraud and Abuse Act (18 U.S.C. § 1030). 
                    This includes unauthorized access to systems without explicit written permission from the owner.
                </p>
            </div>

            <h2>Authorized Use Only</h2>
            <div class="authorized">
                <p><strong>This system is intended ONLY for:</strong></p>
                <ul>
                    <li>Authorized penetration testing (with written permission)</li>
                    <li>Educational projects in controlled environments</li>
                    <li>Security research on systems you own</li>
                    <li>Authorized red team exercises</li>
                    <li>Proof-of-concept demonstrations on test networks</li>
                </ul>
            </div>

            <h2>Prohibited Uses</h2>
            <div class="warning">
                <p><strong>Strictly prohibited:</strong></p>
                <ul>
                    <li>Testing against systems without explicit written permission</li>
                    <li>Unauthorized access to any computer system</li>
                    <li>Disruption of services or data destruction</li>
                    <li>Deployment against systems you don't own or operate</li>
                    <li>Any use that violates local, state, or federal law</li>
                </ul>
            </div>

            <h2>Legal Liability</h2>
            <p>Users of this software are solely responsible for their actions. The developers/authors are not liable for:</p>
            <ul>
                <li>Unauthorized use of this system</li>
                <li>Violations of the CFAA or other laws</li>
                <li>Damage caused by this system</li>
                <li>Any penalties, fines, or imprisonment resulting from misuse</li>
            </ul>

            <h2>Responsible Disclosure</h2>
            <p>If you discover vulnerabilities through authorized testing:</p>
            <ul>
                <li>Follow the organization's responsible disclosure policy</li>
                <li>Report privately to the affected organization</li>
                <li>Allow time for patching before public disclosure</li>
                <li>Document your testing scope and authorization</li>
            </ul>

            <h2>Academic & Research Use</h2>
            <p>For academic projects:</p>
            <ul>
                <li>Include ethical approval documentation</li>
                <li>Work only in controlled lab environments</li>
                <li>Document your institutional oversight</li>
                <li>Maintain detailed logs of all testing activities</li>
                <li>Only use test systems you control</li>
            </ul>

            <h2>Deployment Responsibility</h2>
            <p>Before deploying this system:</p>
            <ul>
                <li>Verify you have authorization for its use</li>
                <li>Understand your legal obligations</li>
                <li>Implement access controls and logging</li>
                <li>Monitor for unauthorized activity</li>
                <li>Keep the system secure from external attacks</li>
            </ul>

            <div class="warning">
                <h3>By using this system, you acknowledge:</h3>
                <ul>
                    <li>You have read and understood this notice</li>
                    <li>You have authorization for your intended use</li>
                    <li>You accept full legal responsibility</li>
                    <li>You understand the CFAA penalties (up to 10 years imprisonment)</li>
                    <li>You agree not to use this system for unauthorized access</li>
                </ul>
            </div>

            <p style="margin-top: 2rem; font-style: italic; color: #666;">
                This is an educational command & control framework for authorized security testing only.
                Unauthorized access to computer systems is illegal.
            </p>
        </div>
    </section>
</body>
</html>
```

## Step 8: Push to GitHub Pages Branch

```bash
# After creating all files above on the gh-pages branch

git add .
git commit -m "Deploy documentation and landing page to GitHub Pages"
git push origin gh-pages
```

## Step 9: Enable GitHub Pages

1. Go to your repository settings
2. Navigate to **Pages** section
3. Select **Deploy from a branch**
4. Choose `gh-pages` branch
5. Click **Save**

Your documentation will be available at: `https://<your_username>.github.io/<repo-name>`

## Step 10: Update Frontend to Use Backend URL

In your PythonAnywhere backend (agent_ui.html and hq_dashboard.html), ensure:

```javascript
// Use the deployed PythonAnywhere URL
const HQ_SERVER_URL = 'https://<your_username>.pythonanywhere.com';
```

## Step 11: CORS Configuration (if needed)

If frontend on GitHub Pages and backend on PythonAnywhere have CORS issues, update main.py:

```python
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
```

Then install flask-cors:
```bash
pip install Flask-CORS
```

## Integration Points

After deploying both:

- **GitHub Pages** hosts:
  - Landing page with backend status indicator
  - API documentation reference
  - Architecture diagrams
  - Ethical use disclaimers

- **PythonAnywhere** hosts:
  - HQ Dashboard (`/`)
  - Agent UI (`/agent-ui`)
  - All API endpoints (`/api/*`)
  - SQLite database
  - File uploads

## Monitoring & Maintenance

### GitHub Pages
- Free tier, automatic deployments via git push
- No backend needed, pure static content
- Check deployment status in repository → Deployments tab

### PythonAnywhere
- Monitor server logs in Web tab
- Check Database size (SQLite has limits on free tier)
- Clear old uploaded files periodically
- Monitor CPU/memory usage

## Next Steps

1. ✅ Deploy backend to PythonAnywhere
2. ✅ Deploy documentation to GitHub Pages
3. Test API connectivity from GitHub Pages frontend
4. Monitor both deployments
5. Set up regular backups of SQLite database

---

**Questions?** Check the [API Documentation](api.html) or review [Deployment Guides](../docs/PYTHONANYWHERE_DEPLOYMENT.md).
