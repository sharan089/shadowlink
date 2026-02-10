import subprocess
import sys
import os
import time
import webbrowser

ROOT = os.getcwd()

def run(cmd, cwd=None):
    subprocess.Popen(cmd, cwd=cwd, shell=True)

print("\n🚀 Starting ShadowLink Demo...\n")

# ---- HQ SERVER ----
hq_dir = os.path.join(ROOT, "hq_server")
run("python -m venv venv", cwd=hq_dir)
run("venv\\Scripts\\pip install -r requirements.txt", cwd=hq_dir)
run("venv\\Scripts\\python main.py", cwd=hq_dir)

time.sleep(4)  # wait for server

# ---- AGENT ----
agent_dir = os.path.join(ROOT, "agent")
run("python -m venv venv", cwd=agent_dir)
run("venv\\Scripts\\pip install -r requirements.txt", cwd=agent_dir)
run("venv\\Scripts\\python agent.py", cwd=agent_dir)

# ---- OPEN BROWSER ----
time.sleep(2)
webbrowser.open("http://127.0.0.1:5000")

print("\n✅ ShadowLink is running!")
print("🌐 Dashboard: http://127.0.0.1:5000")
print("🕵️ Agent is connecting...\n")
