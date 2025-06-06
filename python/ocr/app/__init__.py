import json
import os
import logging
from threading import Thread

from flask import Flask, current_app
from flask_cors import CORS
from flask_migrate import Migrate


migrate = Migrate()
cors = CORS()

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
            r"/api/ocr/*": {
                "origins": ["http://localhost:8080", "http://localhost"],
                "supports_credentials": True,
                "allow_headers": ["Content-Type", "X-CSRFToken"],
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

    from .ocr_api import ocr as ocr_blueprint

    app.register_blueprint(ocr_blueprint)

    return app
