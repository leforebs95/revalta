import os
import logging
import json
import yaml

import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def get_aws_secret(aws_session, secret_name, region_name):
    logger.info(f"Fetching AWS secret: {secret_name} from region: {region_name}")
    client = aws_session.client(service_name="secretsmanager", region_name=region_name)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        logger.info(f"Successfully retrieved secret: {secret_name}")
    except ClientError as e:
        logger.error(f"Failed to retrieve secret: {secret_name}, error: {e}")
        raise e

    return json.loads(get_secret_value_response["SecretString"])


def get_db_connection_vars(aws_session):
    # You can make this configurable through environment variables
    secret_name = os.environ.get("DB_SECRET", None)
    connection_secret_name = os.environ.get("DB_CONNECTION_SECRET", None)
    region_name = "us-west-2"
    logger.info(f"Fetching DB connection variables from secret: {secret_name}")

    try:
        secret_data = get_aws_secret(aws_session, secret_name, region_name)
        connection_secret_data = get_aws_secret(
            aws_session, connection_secret_name, region_name
        )
        logger.info("Successfully fetched DB connection variables")
    except Exception as e:
        logger.error(f"Failed to fetch DB connection variables, error: {e}")
        raise e

    connection_vars = {**secret_data, **connection_secret_data}
    return connection_vars


def get_oauth_vars(aws_session):
    secret_name = os.environ.get("OAUTH_SECRET", None)
    region_name = "us-west-2"
    logger.info(f"Fetching OAuth variables from secret: {secret_name}")

    try:
        secret_data = get_aws_secret(aws_session, secret_name, region_name)
        logger.info("Successfully fetched OAuth variables")
    except Exception as e:
        logger.error(f"Failed to fetch OAuth variables, error: {e}")
        raise e

    return secret_data


def get_config():
    """
    Retrieves and constructs the configuration for the application.
    This function performs the following steps:
    1. Reads the common configuration.
    2. Adds AWS session credentials from environment variables to the configuration.
    3. Establishes an AWS session using the provided credentials.
    4. Retrieves and updates database connection variables in the configuration.
    Returns:
        dict: The complete configuration dictionary.
    Raises:
        Exception: If reading the common configuration or updating the DB connection variables fails.
    """
    logger.info("Starting to get configuration")

    if os.environ.get("ENVIRONMENT") == "local":
        load_dotenv()
        logger.info("Loaded environment variables from .env file")

    common_config = dict()

    common_config["aws_session"] = {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", None),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", None),
        "aws_session_token": os.environ.get("AWS_SESSION_TOKEN", None),
    }

    aws_session = boto3.session.Session(**common_config["aws_session"])

    try:
        db_vars = get_db_connection_vars(aws_session)
        common_config["db"] = db_vars
        logger.info("DB connection variables updated successfully")
    except Exception as e:
        logger.error(f"Failed to update DB connection variables, error: {e}")
        raise e

    try:
        oauth_vars = get_oauth_vars(aws_session)
        common_config["oauth"] = oauth_vars
        logger.info("OAuth variables updated successfully")
    except Exception as e:
        logger.error(f"Failed to update OAuth variables, error: {e}")
        raise e
    logger.info("Configuration successfully retrieved")
    return common_config
