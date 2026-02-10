# PythonAnywhere Deployment Guide

This guide walks you through deploying ShadowLink's Flask backend to PythonAnywhere.

## Prerequisites

- PythonAnywhere account (free or paid)
- GitHub account with your ShadowLink repository
- Git installed locally

## Step 1: Create PythonAnywhere Account

1. Go to https://www.pythonanywhere.com
2. Click "Sign up for a Beginner account" (free tier available)
3. Verify your email
4. Log in to your dashboard

## Step 2: Clone Your Repository

In PythonAnywhere Bash console:

```bash
cd /home/<your_username>
git clone https://github.com/<your_username>/shadowlink.git
cd shadowlink
```

## Step 3: Create Virtual Environment

```bash
mkvirtualenv --python=/usr/bin/python3.10 shadowlink-env
```

Activate it:
```bash
workon shadowlink-env
```

## Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 5: Configure the Web App

1. Go to **Web** tab in PythonAnywhere dashboard
2. Click **Add a new web app**
3. Choose **Manual configuration**
4. Select **Python 3.10**
5. Click through to create the app

This creates:
- Web app at `https://<your_username>.pythonanywhere.com`
- WSGI configuration file at `/var/www/<your_username>_pythonanywhere_com_wsgi.py`

## Step 6: Update WSGI File

Edit `/var/www/<your_username>_pythonanywhere_com_wsgi.py`:

```python
import sys
import os

# Add your project to the path
project_home = '/home/<your_username>/shadowlink'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Set environment variables
os.environ['FLASK_APP'] = 'hq_server/main.py'
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from hq_server.main import app as application
```

## Step 7: Configure Web App Settings

In the **Web** tab:

1. **Virtualenv path**: `/home/<your_username>/.virtualenvs/shadowlink-env`
2. **Source code**: `/home/<your_username>/shadowlink`
3. **Working directory**: `/home/<your_username>/shadowlink/hq_server`

## Step 8: Create Database Directory

The SQLite database needs write permissions:

```bash
mkdir -p /home/<your_username>/shadowlink/hq_server
chmod 775 /home/<your_username>/shadowlink/hq_server
```

## Step 9: Initialize Database

```bash
cd /home/<your_username>/shadowlink/hq_server
python << 'EOF'
from main import app, db, init_db
with app.app_context():
    init_db(app)
    print("Database initialized successfully")
EOF
```

## Step 10: Reload Web App

1. Go to **Web** tab
2. Click the **Reload** button for your web app
3. Wait 30 seconds for reload to complete

## Step 11: Test Your Deployment

Visit `https://<your_username>.pythonanywhere.com`

You should see:
- HQ Dashboard at `/` 
- Agent UI at `/agent-ui`
- API endpoints responding at `/api/*`

### Test API:

```bash
curl https://<your_username>.pythonanywhere.com/api/agents

# Or from your browser console:
fetch('https://<your_username>.pythonanywhere.com/api/agents')
  .then(r => r.json())
  .then(d => console.log(d))
```

## Step 12: Update Frontend API URLs (Important!)

In your agent_ui.html and hq_dashboard.html, update the HQ_SERVER_URL:

**Before (local):**
```javascript
const HQ_SERVER_URL = 'http://localhost:5000';
```

**After (PythonAnywhere):**
```javascript
const HQ_SERVER_URL = 'https://<your_username>.pythonanywhere.com';
```

Or make it dynamic:
```javascript
const HQ_SERVER_URL = window.location.origin;
```

## Step 13: Database Persistence

The SQLite database is stored at:
```
/home/<your_username>/shadowlink/hq_server/shadowlink.db
```

Free tier note: PythonAnywhere has disk limits. Monitor your storage:
- Free tier: 512 MB total
- Each agent upload counts toward this limit

**Recommendation**: For production, migrate to PostgreSQL (available on PythonAnywhere paid plans).

## Step 14: File Upload Storage

Create uploads directory:
```bash
mkdir -p /home/<your_username>/shadowlink/hq_server/uploads
chmod 777 /home/<your_username>/shadowlink/hq_server/uploads
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'hq_server'"

Solution: Ensure working directory is set to `hq_server` in Web tab settings.

### Database locked errors

Solution: Reduce concurrent requests. Use PostgreSQL on paid plans.

### Static files not loading

Solution: Configure static files in **Web** tab:
- URL: `/static/`
- Directory: `/home/<your_username>/shadowlink/hq_server/static`

### 500 Internal Server Error

Check error logs in **Web** tab → **Error log** and **Server log**

## Monitoring

1. **CPU/Memory**: Go to **Web** tab → Statistics
2. **Error logs**: Web tab → Error log
3. **Access logs**: Web tab → Server log

## Performance Optimization

For free tier with limitations:
1. Reduce refresh rate in hq_dashboard.html from 1s to 5s
2. Limit number of concurrent agents
3. Clean up old uploads regularly
4. Use file archival strategy

```javascript
// In hq_dashboard.html, change:
setInterval(loadAgents, 5000);  // 5 seconds instead of 1
```

## Upgrading to Paid Plan

Benefits:
- More disk space (2+ GB)
- Better CPU/Memory allocation
- PostgreSQL database option
- Higher daily bandwidth limits
- Always-on processes

Upgrade in **Account** tab.

## Next Steps

1. Deploy frontend to GitHub Pages (see GITHUB_PAGES_DEPLOYMENT.md)
2. Set up PostgreSQL if on paid plan
3. Configure custom domain (if on paid plan)
4. Set up monitoring/logging alerts
5. Regular database backups (download .db file)

## Important Notes

⚠️ **Security Reminders**:
- Keep API keys secret (not in version control)
- Don't commit database passwords
- Use environment variables for sensitive data
- Monitor for unauthorized agents/connections
- Review ETHICAL_USE.md before operational use

---

**Support**: Issues with PythonAnywhere? Check their help forum: https://www.pythonanywhere.com/forums/
