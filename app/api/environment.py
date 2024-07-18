import os
import json
import yaml

import boto3
from botocore.exceptions import ClientError


def get_aws_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session(
        aws_access_key_id="ASIA6GBMARJ6EV3PRBNV",
        aws_secret_access_key="914kEVCLTArTPXMA2LSwexaCh2vRmE6A+vCpRYxs",
        aws_session_token="IQoJb3JpZ2luX2VjECwaCXVzLXdlc3QtMiJHMEUCIBH8o+bNEvUO0/pz3V3WzVospf7ojMkO7/2Yei344nM6AiEA9xlMyBHGQyU0n2GxuZGAGaAG+X+JKscU4D+BR3jqKRIq9AII9f//////////ARAAGgw5NzUwNDk4ODYzMzIiDJdA1Vybc+uipSEI6irIAnxn5M5BA2ge6s8wsLC4ysPWZG9Vc53XYmuvkjQtVEWZi7pgQetRm6pZBG/BM6Il9Ur17jpXii/Uo9KMERVMiznaUuMWGghYGH3K8qKqcW222DjO6kCZk8ZA6dppNTrgOHjv6e7W8qeRvWKVmb0aczk7Yxyh/HiB/Jd5gHRazG3gsHSzHvHB3/QKMH/TKwaSo3maziuGZhvvZwcdqKa4lXbV/BwoF5NBIDEQOtopB38RDVidR4tN+3LRaivlD3L+14j5rKGb/OFsEernTXi6cob6LYxm/yKrsTgOXm99ziraRjUm3NPFVHQNGNc9t4RYOSCzxjwLGeBJCT21sAQZz6GV0RKlDoUIzVpMTH91ritB3wsyWSKhWBCefevOHC5GmoecSHx9LkxvxqfR0JWBAUBol9kbEC9glbQbBXmTa9Q0Q6vyz5cpbfow58ngtAY6pwHRK7fckNn78YRJ1XX3o0R2JrbL3gbJUC8n4gYdyuiven0XSkzBuYUH8sKFvnhafd/dUZ/2yv1J+S7FWbx/Pjq0mBt4zfo/L280lYYmklojkqCsc4+hYPvArW80YfhRVqN6kaP7s0TAKqCpmmcMWOEBhYhqtcGMLQ9gWnncYbHChH8Nrl0rmIFumqtJmN83usHnHu70j9wch3MqxemQqS3ZDLRnBAFf7Q==",
    )
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
