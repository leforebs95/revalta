"""
AWS Secrets Manager client module for managing secrets.

This module provides a simple interface to interact with AWS Secrets Manager,
including operations for creating, retrieving, updating, and deleting secrets.
"""

import json
import logging
from typing import Optional, Dict, Any, List

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class SecretsManagerError(Exception):
    """Base exception class for Secrets Manager operations."""

    pass


class SecretNotFoundError(SecretsManagerError):
    """Raised when a secret is not found."""

    pass


class SecretVersionNotFoundError(SecretsManagerError):
    """Raised when a specific version of a secret is not found."""

    pass


class SecretsManagerClient:
    """
    A client for interacting with AWS Secrets Manager.

    Args:
        region_name (str): AWS region name
        profile_name (Optional[str]): AWS profile name
        session (Optional[boto3.Session]): Boto3 session object
    """

    def __init__(
        self,
        region_name: str,
        profile_name: Optional[str] = None,
        session: Optional[boto3.Session] = None,
    ) -> None:
        self._session = session or boto3.Session(
            profile_name=profile_name, region_name=region_name
        )
        self._client = self._session.client("secretsmanager")

    def create_secret(
        self,
        secret_name: str,
        secret_value: Dict[str, Any],
        description: Optional[str] = None,
        tags: Optional[List[Dict[str, str]]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new secret.

        Args:
            secret_name (str): Name of the secret
            secret_value (Dict[str, Any]): Value to be stored in the secret
            description (Optional[str]): Description of the secret
            tags (Optional[List[Dict[str, str]]]): List of tags to attach to the secret

        Returns:
            Dict[str, Any]: Response from AWS Secrets Manager

        Raises:
            SecretsManagerError: If the secret creation fails
        """
        try:
            kwargs = {"Name": secret_name, "SecretString": json.dumps(secret_value)}

            if description:
                kwargs["Description"] = description
            if tags:
                kwargs["Tags"] = tags

            response = self._client.create_secret(**kwargs)
            logger.info(f"Created secret: {secret_name}")
            return response

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            logger.error(
                f"Failed to create secret {secret_name}: {error_code} - {error_message}"
            )
            raise SecretsManagerError(f"Failed to create secret: {error_message}")

    def get_secret(
        self,
        secret_name: str,
        version_id: Optional[str] = None,
        version_stage: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Retrieve a secret value.

        Args:
            secret_name (str): Name of the secret to retrieve
            version_id (Optional[str]): Specific version ID of the secret
            version_stage (Optional[str]): Specific version stage of the secret

        Returns:
            Dict[str, Any]: Decoded secret value

        Raises:
            SecretNotFoundError: If the secret doesn't exist
            SecretVersionNotFoundError: If the specified version doesn't exist
            SecretsManagerError: For other errors
        """
        try:
            kwargs = {"SecretId": secret_name}

            if version_id:
                kwargs["VersionId"] = version_id
            if version_stage:
                kwargs["VersionStage"] = version_stage

            response = self._client.get_secret_value(**kwargs)
            secret_string = response["SecretString"]
            return json.loads(secret_string)

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]

            if error_code == "ResourceNotFoundException":
                raise SecretNotFoundError(f"Secret {secret_name} not found")
            elif (
                error_code == "InvalidRequestException"
                and "version" in error_message.lower()
            ):
                raise SecretVersionNotFoundError(
                    f"Version not found for secret {secret_name}"
                )
            else:
                logger.error(
                    f"Failed to get secret {secret_name}: {error_code} - {error_message}"
                )
                raise SecretsManagerError(f"Failed to get secret: {error_message}")

    def update_secret(
        self,
        secret_name: str,
        secret_value: Dict[str, Any],
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing secret.

        Args:
            secret_name (str): Name of the secret to update
            secret_value (Dict[str, Any]): New value for the secret
            description (Optional[str]): New description for the secret

        Returns:
            Dict[str, Any]: Response from AWS Secrets Manager

        Raises:
            SecretNotFoundError: If the secret doesn't exist
            SecretsManagerError: For other errors
        """
        try:
            kwargs = {"SecretId": secret_name, "SecretString": json.dumps(secret_value)}

            if description:
                kwargs["Description"] = description

            response = self._client.update_secret(**kwargs)
            logger.info(f"Updated secret: {secret_name}")
            return response

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]

            if error_code == "ResourceNotFoundException":
                raise SecretNotFoundError(f"Secret {secret_name} not found")
            else:
                logger.error(
                    f"Failed to update secret {secret_name}: {error_code} - {error_message}"
                )
                raise SecretsManagerError(f"Failed to update secret: {error_message}")

    def delete_secret(
        self,
        secret_name: str,
        force_delete: bool = False,
        recovery_window_in_days: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Delete a secret.

        Args:
            secret_name (str): Name of the secret to delete
            force_delete (bool): If True, immediately deletes the secret without recovery
            recovery_window_in_days (Optional[int]): Number of days before permanent deletion

        Returns:
            Dict[str, Any]: Response from AWS Secrets Manager

        Raises:
            SecretNotFoundError: If the secret doesn't exist
            SecretsManagerError: For other errors
        """
        try:
            kwargs = {"SecretId": secret_name}

            if force_delete:
                kwargs["ForceDeleteWithoutRecovery"] = True
            elif recovery_window_in_days is not None:
                kwargs["RecoveryWindowInDays"] = recovery_window_in_days

            response = self._client.delete_secret(**kwargs)
            logger.info(f"Deleted secret: {secret_name}")
            return response

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]

            if error_code == "ResourceNotFoundException":
                raise SecretNotFoundError(f"Secret {secret_name} not found")
            else:
                logger.error(
                    f"Failed to delete secret {secret_name}: {error_code} - {error_message}"
                )
                raise SecretsManagerError(f"Failed to delete secret: {error_message}")

    def list_secrets(
        self, max_results: Optional[int] = None, tags: Optional[Dict[str, str]] = None
    ) -> List[Dict[str, Any]]:
        """
        List all secrets in the account.

        Args:
            max_results (Optional[int]): Maximum number of secrets to return
            tags (Optional[Dict[str, str]]): Filter secrets by tags

        Returns:
            List[Dict[str, Any]]: List of secrets

        Raises:
            SecretsManagerError: If the operation fails
        """
        try:
            kwargs = {}
            if max_results:
                kwargs["MaxResults"] = max_results
            if tags:
                kwargs["Filters"] = [{"Key": "tag-key", "Values": list(tags.keys())}]

            secrets = []
            paginator = self._client.get_paginator("list_secrets")

            for page in paginator.paginate(**kwargs):
                secrets.extend(page.get("SecretList", []))

                if max_results and len(secrets) >= max_results:
                    secrets = secrets[:max_results]
                    break

            return secrets

        except ClientError as e:
            error_code = e.response["Error"]["Code"]
            error_message = e.response["Error"]["Message"]
            logger.error(f"Failed to list secrets: {error_code} - {error_message}")
            raise SecretsManagerError(f"Failed to list secrets: {error_message}")
