from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    CORS(app)
    
    # Default configuration
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/chat'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        VECTOR_API_URL=os.getenv('VECTOR_API_URL', 'http://vector-api:5000'),
        ANTHROPIC_API_KEY=os.getenv('ANTHROPIC_API_KEY')
    )
    
    # Override with any passed config
    if config:
        app.config.update(config)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    from .chat_api import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app 