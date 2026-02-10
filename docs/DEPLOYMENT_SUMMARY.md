# ShadowLink Deployment Guide

Complete guide to deploying ShadowLink across two platforms for maximum flexibility.

## Quick Overview

**ShadowLink** is deployed in a hybrid architecture:

```
┌─────────────────────────────────────────┐
│  GitHub Pages (Static Content)          │
│  - Documentation site                   │
│  - Landing page with status indicator   │
│  - API reference guide                  │
│  URL: https://<user>.github.io/shadowlink
└─────────────────────────────────────────┘
           │ Frontend calls backend
           ▼
┌─────────────────────────────────────────┐
│  PythonAnywhere (Flask Backend)         │
│  - HQ Dashboard UI                      │
│  - Agent UI                             │
│  - REST API (20+ endpoints)             │
│  - SQLite Database                      │
│  URL: https://<user>.pythonanywhere.com
└─────────────────────────────────────────┘
           │ HTTP Polling
           ▼
      ┌─────┴──────┐
      ▼            ▼
    Agent 1      Agent 2        (Remote agents)
```

## Deployment Prerequisites

1. **GitHub Account**: For version control & GitHub Pages
2. **PythonAnywhere Account**: For Flask backend (free tier available)
3. **Git**: Installed and configured on your local machine
4. **Python 3.10+**: For development (PythonAnywhere uses 3.10)

## Platform Comparison

| Feature | GitHub Pages | PythonAnywhere |
|---------|--------------|----------------|
| **Type** | Static hosting | Python server |
| **Cost** | Free | Free/Paid |
| **What runs** | HTML, CSS, JS only | Flask backend |
| **Database** | None | SQLite (free) |
| **File uploads** | Not supported | Yes (disk limited) |
| **API access** | Read-only | Full access |

## Deployment Option 1: Backend Only (Local Development)

Run everything locally:

```bash
cd hq_server
pip install -r ../requirements.txt
python main.py
```

Access at `http://localhost:5000`

**Best for**: Testing, development, demonstrations

---

## Deployment Option 2: Backend on PythonAnywhere + GitHub Pages Documentation

This is the **recommended approach** for public deployment.

### Step 1: Deploy Backend to PythonAnywhere

Follow the detailed guide: [PYTHONANYWHERE_DEPLOYMENT.md](PYTHONANYWHERE_DEPLOYMENT.md)

Time: ~15-20 minutes

**Checklist:**
- [ ] PythonAnywhere account created
- [ ] Repository cloned to PythonAnywhere
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Web app configured
- [ ] Backend running at `https://<user>.pythonanywhere.com`

### Step 2: Deploy Documentation to GitHub Pages

Follow the detailed guide: [GITHUB_PAGES_DEPLOYMENT.md](GITHUB_PAGES_DEPLOYMENT.md)

Time: ~10-15 minutes

**Checklist:**
- [ ] `gh-pages` branch created
- [ ] Documentation files created
- [ ] GitHub Pages enabled in settings
- [ ] Landing page accessible at `https://<user>.github.io/shadowlink`
- [ ] Backend status indicator working

### Step 3: Update Frontend API Endpoints

Update both HTML files to point to deployed backend:

**In hq_dashboard.html (line ~50):**
```javascript
const HQ_SERVER_URL = 'https://<your_username>.pythonanywhere.com';
```

**In agent_ui.html (line ~50):**
```javascript
const HQ_SERVER_URL = 'https://<your_username>.pythonanywhere.com';
```

Or make it dynamic:
```javascript
// Auto-detect backend from current location
const HQ_SERVER_URL = window.location.origin.includes('github.io') 
  ? 'https://<your_username>.pythonanywhere.com'
  : window.location.origin;
```

### Step 4: Handle CORS (if needed)

If you get CORS errors, update PythonAnywhere backend:

**In /hq_server/main.py (after imports):**
```python
from flask_cors import CORS
CORS(app)
```

**Install in PythonAnywhere:**
```bash
pip install Flask-CORS
```

---

## Deployment Option 3: Complete Cloud (Backend + Frontend)

Deploy everything to one PythonAnywhere instance:

1. All files already in `/hq_server`
2. Routes already configured:
   - `/` → HQ Dashboard
   - `/agent-ui` → Agent UI
   - `/api/*` → API endpoints

Access directly at `https://<user>.pythonanywhere.com`

(No need for GitHub Pages in this scenario)

---

## Post-Deployment Verification

### Test Backend API

```bash
# List agents
curl https://<user>.pythonanywhere.com/api/agents

# From browser console:
fetch('https://<user>.pythonanywhere.com/api/agents')
  .then(r => r.json())
  .then(d => console.log(d))
```

### Test Dashboard Access

1. Visit `https://<user>.pythonanywhere.com/`
2. You should see the HQ Dashboard
3. Create an agent (should get registration code)
4. Visit `/agent-ui` in another tab
5. Login with registration code
6. Verify heartbeat and command polling work

### Test GitHub Pages

1. Visit `https://<user>.github.io/<repo-name>`
2. See landing page with status indicator
3. Status should show ✅ (green) if backend is accessible
4. Click "Open HQ Dashboard" link

---

## Storage & Limits

### Free Tier Constraints

**GitHub Pages:**
- 1 GB total repo size
- Unlimited pages
- Automatic deploys with `git push`

**PythonAnywhere (Free):**
- 512 MB disk space
- SQLite database included
- Limited CPU (100 seconds/day)
- Limited bandwidth
- No custom domain

**When to upgrade:**
- Agent upload files exceed 100 MB
- Need database larger than SQLite
- Want daily CPU > 100 seconds
- Need always-on processes
- Want custom domain

---

## Database Management

### Backup SQLite Database

From PythonAnywhere Bash:

```bash
# Run manually
cd /home/<user>/shadowlink/hq_server
cp shadowlink.db shadowlink_backup_$(date +%Y%m%d).db

# Or use scheduled task for nightly backups
```

### Monitor Database Size

In PythonAnywhere Web tab, check:
- Disk usage → `shadowlink.db` file size
- Free space remaining

### Clear Old Data

```bash
# Connect via SSH/Bash
python << 'EOF'
from main import app, db, Intelligence
from datetime import datetime, timedelta

with app.app_context():
    # Delete intel older than 30 days
    cutoff_date = datetime.utcnow() - timedelta(days=30)
    deleted = Intelligence.query.filter(
        Intelligence.created_at < cutoff_date
    ).delete()
    db.session.commit()
    print(f"Deleted {deleted} old intelligence records")
EOF
```

---

## Monitoring & Maintenance

### Weekly Checks

- [ ] Backend HTTP status: `curl https://<user>.pythonanywhere.com/api/agents`
- [ ] Database size (PythonAnywhere → Web → Statistics)
- [ ] Error logs for issues
- [ ] Agent connectivity (any stuck offline?)

### Monthly Maintenance

- [ ] Archives old uploaded files
- [ ] Backup database
- [ ] Update dependencies: `pip list --outdated`
- [ ] Review access logs for suspicious activity
- [ ] Review ETHICAL_USE.md compliance

### Quarterly Scale Review

- [ ] Is free tier sufficient?
- [ ] Should upgrade database to PostgreSQL?
- [ ] Should migrate to custom domain?
- [ ] Should increase CPU allocation?

---

## Troubleshooting

### Backend Won't Start

**Error:** 500 Internal Server Error

**Solutions:**
1. Check error logs: PythonAnywhere → Web → Error log
2. Verify dependencies: `pip list | grep -E 'Flask|SQLAlchemy'`
3. Check database permissions: `ls -la shadowlink.db`
4. Reload web app: PythonAnywhere → Web → Reload button

### File Upload Fails

**Error:** "413 Payload Too Large" or "Insufficient disk space"

**Solutions:**
1. Check free space: PythonAnywhere → Web → Statistics
2. Delete old uploads: `rm hq_server/uploads/old_*`
3. Upgrade to paid plan for more space

### CORS Errors (GitHub Pages → PythonAnywhere)

**Error:** "Access to XMLHttpRequest blocked by CORS policy"

**Solution:**
```python
# In /hq_server/main.py
from flask_cors import CORS
CORS(app, origins=['https://<user>.github.io'])
```

### Agent Stuck Offline

**Symptoms:** Agent shows offline even though it's sending heartbeats

**Solutions:**
1. Check last_heartbeat timestamp in database
2. Verify IP address is correct
3. Check heartbeat timeout (60 seconds default)
4. Reload agent UI page to restart heartbeat

---

## Security Checklist

Before production deployment:

- [ ] Read ETHICAL_USE.md and understand legal implications
- [ ] Change default config settings (host, port, debug mode)
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (PythonAnywhere does this automatically)
- [ ] Implement rate limiting (future enhancement)
- [ ] Set up logging and monitoring
- [ ] Regular database backups
- [ ] Restrict agent creation to authorized users (future)

---

## Migration Path

If you start local and want to scale:

1. **Local** → Works fine, easy development
2. **PythonAnywhere free** → Add public backend, 512 MB storage
3. **PythonAnywhere paid** → PostgreSQL support, more CPU, custom domain
4. **VPS (Digital Ocean/AWS)** → Full control, Docker, scaling

For this project, **PythonAnywhere free tier is sufficient** for:
- Up to 10 active agents
- Light file uploads (< 100 MB total)
- Educational/testing purposes
- Proof-of-concept demonstrations

---

## Support & Resources

- **PythonAnywhere Docs**: https://help.pythonanywhere.com/
- **PythonAnywhere Forums**: https://www.pythonanywhere.com/forums/
- **GitHub Pages Docs**: https://pages.github.com/
- **Flask Documentation**: https://flask.palletsprojects.com/
- **GitHub Support**: https://support.github.com/

---

## Summary

| Step | Platform | Time | Difficulty |
|------|----------|------|-----------|
| 1. Backend | PythonAnywhere | 15-20m | Medium |
| 2. Docs | GitHub Pages | 10-15m | Easy |
| 3. Integration | Both | 5-10m | Easy |
| **Total** | **Both** | **~40m** | **Medium** |

After deployment, you'll have:
- ✅ Public backend API
- ✅ Public documentation site
- ✅ Distributed agent capability
- ✅ Real-time command & control
- ✅ File upload/download support

For questions, refer to platform-specific guides:
- Backend issues → [PYTHONANYWHERE_DEPLOYMENT.md](PYTHONANYWHERE_DEPLOYMENT.md)
- Documentation issues → [GITHUB_PAGES_DEPLOYMENT.md](GITHUB_PAGES_DEPLOYMENT.md)
