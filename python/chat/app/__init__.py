from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

migrate = Migrate()
db = SQLAlchemy()

def create_app(config=None):
    app = Flask(__name__)
    CORS(app)
    
    # Default configuration
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv('DATABASE_URL', 'postgresql://local_chat_user:local_chat_pass@local-chat-db:5432/chat'),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        VECTOR_API_URL=os.getenv('VECTOR_API_URL', 'http://vector-api:5003'),
        ANTHROPIC_API_KEY=os.getenv('ANTHROPIC_API_KEY')
    )
    
    # Override with any passed config
    if config:
        app.config.update(config)
    
    # Initialize extensions
    db.init_app(app)

    with app.app_context():
        # Create database tables
        db.create_all()
    
    migrate.init_app(app, db)

    # Register blueprints
    from .chat_api import chat as chat_blueprint
    app.register_blueprint(chat_blueprint)
    
    
    return app 