import os
import json
import yaml

import boto3
from botocore.exceptions import ClientError


def get_aws_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=region_name)

    print(client.list_secrets().get("SecretList"))

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    return json.loads(get_secret_value_response["SecretString"])


def read_common_config():
    config_path = os.path.join(os.path.dirname(__file__), "..", "config/common.yml")

    with open(config_path, "r") as file:
        config_data = yaml.safe_load(file)

    return config_data


def get_db_connection_vars():
    secret_name = "rds!db-8c5cf11e-e74e-40e8-aa10-2b53b54c8a71"

    region_name = "us-west-2"
    user_pass_secret = get_aws_secret(secret_name, region_name)

    return user_pass_secret


def get_config():
    common_config = read_common_config()
    common_config["db"].update(get_db_connection_vars())

    return common_config
