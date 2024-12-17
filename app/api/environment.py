import os
import logging
import json
import yaml

import boto3
from botocore.exceptions import ClientError

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


def read_common_config():
    config_path = os.path.join(os.path.dirname(__file__), "config/common.yml")
    logger.info(f"Reading common configuration from: {config_path}")

    try:
        with open(config_path, "r") as file:
            config_data = yaml.safe_load(file)
            logger.info("Successfully read common configuration")
    except Exception as e:
        logger.error(f"Failed to read common configuration, error: {e}")
        raise e

    return config_data


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
        connection_vars = {
            "username": secret_data["username"],
            "password": secret_data["password"],
            "db-name": secret_data["dbname"],
            "engine": secret_data.get("engine", "mysql"),
            "host": connection_secret_data["host"],
            "port": connection_secret_data["port"],
        }
        logger.info("Successfully fetched DB connection variables")
    except Exception as e:
        logger.error(f"Failed to fetch DB connection variables, error: {e}")
        raise e

    return connection_vars


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

    try:
        common_config = read_common_config()
        logger.info("Common configuration read successfully")
    except Exception as e:
        logger.error(f"Failed to read common configuration, error: {e}")
        raise e

    common_config["aws_session"] = {
        "aws_access_key_id": os.environ.get("AWS_ACCESS_KEY_ID", None),
        "aws_secret_access_key": os.environ.get("AWS_SECRET_ACCESS_KEY", None),
        "aws_session_token": os.environ.get("AWS_SESSION_TOKEN", None),
    }

    aws_session = boto3.session.Session(**common_config["aws_session"])

    try:
        db_vars = get_db_connection_vars(aws_session)
        common_config["db"].update(db_vars)
        logger.info("DB connection variables updated successfully")
    except Exception as e:
        logger.error(f"Failed to update DB connection variables, error: {e}")
        raise e

    logger.info("Configuration successfully retrieved")
    return common_config
