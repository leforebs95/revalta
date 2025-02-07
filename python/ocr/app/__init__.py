import json
import os
import logging
from threading import Thread

from flask import Flask, current_app
from flask_cors import CORS
from flask_migrate import Migrate
import redis

from utils.ocr_processor import OCRProcessor

migrate = Migrate()
cors = CORS()
processor = OCRProcessor()

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def create_app():
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

    from .models import db
    from .models import DocumentPage

    db.init_app(app)
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db)

    # Set up Redis connection
    app.redis = redis.Redis(
        host=app.config["REDIS_HOST"],
        port=app.config["REDIS_PORT"],
        decode_responses=True,
    )

    from .ocr_api.routes import start_listener

    app_context = app.app_context()

    def run_listener():
        with app_context:
            start_listener()

    Thread(target=run_listener, daemon=True).start()

    from .ocr_api import ocr as ocr_blueprint

    app.register_blueprint(ocr_blueprint)

    return app
