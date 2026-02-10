"""
Database Models and Setup
SQLAlchemy models for persistence
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

class Agent(db.Model):
    """Agent model"""
    __tablename__ = 'agents'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = db.Column(db.String(100), unique=True, nullable=False)
    registration_code = db.Column(db.String(32), unique=True, nullable=False)
    api_key = db.Column(db.String(64), unique=True, nullable=False)
    status = db.Column(db.String(20), default='offline')  # online, offline
    last_heartbeat = db.Column(db.DateTime, default=datetime.utcnow)
    registered_at = db.Column(db.DateTime, default=datetime.utcnow)
    agent_metadata = db.Column(db.JSON, default=dict)
    
    # Relations
    commands = db.relationship('Command', back_populates='agent', cascade='all, delete-orphan')
    intel = db.relationship('Intelligence', back_populates='agent', cascade='all, delete-orphan')
    messages = db.relationship('Message', back_populates='agent', cascade='all, delete-orphan')

class Command(db.Model):
    """Command model"""
    __tablename__ = 'commands'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    command_id = db.Column(db.String(50), unique=True, nullable=False)
    agent_id = db.Column(db.String(36), db.ForeignKey('agents.id'), nullable=False)
    command_type = db.Column(db.String(50), nullable=False)
    payload = db.Column(db.JSON, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, executing, completed, failed
    result = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    executed_at = db.Column(db.DateTime, nullable=True)
    
    agent = db.relationship('Agent', back_populates='commands')

class Intelligence(db.Model):
    """Intelligence data model"""
    __tablename__ = 'intelligence'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = db.Column(db.String(36), db.ForeignKey('agents.id'), nullable=False)
    data_type = db.Column(db.String(50), nullable=False)  # system_info, network_info, files, etc
    data = db.Column(db.JSON, nullable=True)
    file_path = db.Column(db.String(500), nullable=True)  # Path to stored file
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    agent = db.relationship('Agent', back_populates='intel')

class Message(db.Model):
    """Message model for agent-HQ communication"""
    __tablename__ = 'messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    agent_id = db.Column(db.String(36), db.ForeignKey('agents.id'), nullable=False)
    direction = db.Column(db.String(20), nullable=False)  # to_agent, from_agent
    message_type = db.Column(db.String(50), nullable=False)
    content = db.Column(db.String(2000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    agent = db.relationship('Agent', back_populates='messages')

def init_db(app):
    """Initialize database"""
    with app.app_context():
        db.init_app(app)
        db.create_all()
