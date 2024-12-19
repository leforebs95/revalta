#!/bin/sh

# Generate and store secret key in Python to handle AWS interactions better
python3 <<EOF
import boto3
import os
from datetime import datetime, timezone
import secrets
from dynamo_db import DynamoDBStore

def setup_flask_secret():
    try:
        new_secret = secrets.token_hex(32)
        def store_flask_secret(environment: str, new_secret: str):
            store = DynamoDBStore(environment)
            return store.put_item(
                item_type="app_secret",
                item_id="flask_secret_key",
                data={"value": new_secret},
                ttl_seconds=None  # No expiration for app secrets
            )
        store_flask_secret("preprod", new_secret)
        # Set in environment
        os.environ['FLASK_SECRET_KEY'] = new_secret
        print(f"Successfully stored and set Flask secret key")
        
    except Exception as e:
        print(f"Error setting up Flask secret: {str(e)}")
        # Fallback to generate secret without storing
        os.environ['FLASK_SECRET_KEY'] = secrets.token_hex(32)
        print("Using fallback secret key")

setup_flask_secret()
EOF

gunicorn --chdir /usr/src/api -c /usr/src/api/gunicorn_dev.py
