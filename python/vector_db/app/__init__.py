import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from utils.db.postgres import PostgresVectorDB

migrate = Migrate()
cors = CORS()
db = SQLAlchemy()

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_app(config=None):
    app = Flask(__name__)

    if aws_env := os.getenv("AWS"):
        if aws_env == "PROD":
            app.config.from_object("config.ProdFlaskConfig")
        elif aws_env == "PREPROD":
            app.config.from_object("config.PreProdFlaskConfig")
        elif aws_env == "DEV":
            app.config.from_object("config.DevFlaskConfig")
        else:
            raise ValueError(f"Invalid AWS environment: {aws_env}")
    else:
        logger.info("No AWS environment detected. Using local configuration.")
        app.config.from_object("config.LocalFlaskConfig")

    cors.init_app(
        app,
        resources={
            r"/api/*": {
                "origins": ["http://localhost:3000"],
                "supports_credentials": True,
                "allow_headers": ["Content-Type"],
                "max_age": 3600,
            }
        },
    )

    # Initialize SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Initialize vector DB service
    app.vector_db = PostgresVectorDB(user_id=None)

    # Register blueprints
    from .vector_api import vector as vector_blueprint
    app.register_blueprint(vector_blueprint)

    return app
