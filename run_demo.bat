@echo off
echo 🚀 Starting ShadowLink Demo...

cd hq_server
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
start cmd /k python main.py

timeout /t 5

cd ../agent
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
start cmd /k python agent.py

start http://127.0.0.1:5000
