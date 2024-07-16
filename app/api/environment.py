import os
import json
import yaml

import boto3
from botocore.exceptions import ClientError


def get_aws_secret(secret_name, region_name):
    # Create a Secrets Manager client
    session = boto3.session.Session(
        aws_access_key_id="ASIA6GBMARJ6HNTZJVX4",
        aws_secret_access_key="3L9JzD8/x8cbSwP/lQXd3pHmVpiOjID2CsMTk6kg",
        aws_session_token="IQoJb3JpZ2luX2VjEAEaCXVzLXdlc3QtMiJGMEQCIEn9rmfeq1DBHmEqlow490iVHl/+st5lsF/I9iL+lyVLAiAL2QJucsB51Ora4/GVAhEGGEbuEtwNOXZdBltXnJulIyr0AgjK//////////8BEAAaDDk3NTA0OTg4NjMzMiIMm5+AwS7vHKwZWPEdKsgCmUgL4CeUwLemTRUvSK3YpbzKdmVhZGzIUMzKU6eIXFcVKdpVUY1aDARFhpw1NN7ht1bONu+4sP/43F4EGi4awKB18+qcP4HkpT7XldRlmxJPFgCBtO7/Jl3yoee7fGEEgLzwICWTDaVn4iQydDOUchOZho+/JBSDvSkLY1RHc549ffVA3AZrGD5squ0rwRk1vIIr34aPkU0dWAnYJnE+hj2JSiaj4R5xMVMx1f+W0jOwI3z77iPJIeqiZbFhuQ1XjZchYM/nRAsBuw9x1td5VkH+KshVxvzDeiJDy8/zyXbkVIRISoD5gNhuj7LsmWiOJremlG0aO2baBEKspFaZJJ1iuqdkz0tL2pbqJkJftJo0n97GPMJU2BDOV2bB2OYcLSHIosT5ZRoKr3akuA2jJO0SOAHHH2RUb2QGf/I4EfGZPP9VZmaDDzC9/Na0BjqoATK0iZPNc8wSfYYy2Kqad79trOtMX7MVYwngOzCXVlHxVK25mLl79ZTEeKpXAtmXhJXta34gwCkwRtHaD7IW2Zv4ebUpTkykzym70umgp2zBVCzZfIyRkHk0VPCzC3k67mwX072bopge441LSH4Oup+RuJUbQ7CWrWtKuXrwyMlz+c3hOcmz6f1JHxORc74Fapl14LbvfQhCVWpgxML/zQruB61nzv3LtQ==",
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
