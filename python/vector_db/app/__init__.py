import os
import logging
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
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
    
    with app.app_context():
        # Create database tables
        db.create_all()
        
        # Initialize vector extension and RLS
        with db.session.connection() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()
            
            # Create function to check if operation is allowed
            conn.execute(text("""
                CREATE OR REPLACE FUNCTION check_user_access()
                RETURNS boolean AS $$
                BEGIN
                    -- Allow access if current_user_id is not set (system operations)
                    -- or if it matches the row's user_id
                    RETURN (
                        CASE 
                            WHEN current_setting('app.current_user_id', TRUE) IS NULL THEN TRUE
                            ELSE user_id = current_setting('app.current_user_id')::integer
                        END
                    );
                END;
                $$ LANGUAGE plpgsql SECURITY DEFINER;
            """))
            
            conn.execute(text("ALTER TABLE documents ENABLE ROW LEVEL SECURITY"))
            conn.execute(text("ALTER TABLE document_chunks ENABLE ROW LEVEL SECURITY"))
            
            # Update policies to use the new access check function
            conn.execute(text("""
                CREATE POLICY IF NOT EXISTS documents_user_isolation ON documents
                FOR ALL USING (check_user_access())
            """))
            conn.execute(text("""
                CREATE POLICY IF NOT EXISTS chunks_user_isolation ON document_chunks
                FOR ALL USING (check_user_access())
            """))
            
            conn.execute(text("""
                CREATE OR REPLACE FUNCTION set_user_id(p_user_id integer)
                RETURNS void AS $$
                BEGIN
                    -- NULL is valid for system operations
                    PERFORM set_config('app.current_user_id', 
                        CASE WHEN p_user_id IS NULL 
                        THEN NULL 
                        ELSE p_user_id::text 
                        END, 
                        false);
                END;
                $$ LANGUAGE plpgsql SECURITY DEFINER
            """))
            conn.commit()
        
        # Initialize vector DB service
        app.vector_db = PostgresVectorDB(user_id=None)
    
    migrate.init_app(app, db)

    # Register blueprints
    from .vector_api import vector as vector_blueprint
    app.register_blueprint(vector_blueprint)

    return app
