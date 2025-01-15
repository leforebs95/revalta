from datetime import datetime, timezone
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class DynamoDBStore:
    """Generic interface for DynamoDB operations."""

    def __init__(self, environment):
        """
        Initialize DynamoDB store.

        Args:
            table_name: Name of DynamoDB table
            partition_key: Name of the partition key (default: 'id')
        """
        self.table_name = f"{environment}-app-state"
        self._dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
        self._table = self._dynamodb.Table(self.table_name)

    def put_item(
        self,
        item_type: str,
        item_id: str,
        data: Dict[str, Any],
        ttl_seconds: Optional[int] = None,
    ) -> bool:
        """
        Store item in DynamoDB.
        """
        try:
            item = {"item_type": item_type, "item_id": item_id, **data}

            if ttl_seconds is not None:
                timestamp = int(datetime.now(timezone.utc).timestamp())
                item["ttl"] = timestamp + ttl_seconds

            self._table.put_item(Item=item)
            logger.info(f"Stored {item_type} item: {item_id}")
            return True

        except ClientError as e:
            logger.error(f"DynamoDB error storing {item_type}: {str(e)}")
            return False

    def get_item(
        self, item_type: str, item_id: str, check_ttl: bool = True
    ) -> Optional[dict]:
        """
        Retrieve item from DynamoDB.
        """
        try:
            response = self._table.get_item(
                Key={"item_type": item_type, "item_id": item_id}
            )

            item = response.get("Item")
            if not item:
                return None

            if check_ttl and "ttl" in item:
                current_time = int(datetime.now(timezone.utc).timestamp())
                if current_time > item["ttl"]:
                    return None

            return item

        except ClientError as e:
            logger.error(f"DynamoDB error retrieving {item_type}: {str(e)}")
            return None

    def delete_item(self, item_type: str, item_id: str) -> bool:
        """
        Delete item from DynamoDB.

        Args:
            item_type: Type of item (partition key)
            item_id: ID of item (sort key)

        Returns:
            bool: True if deletion successful
        """
        try:
            self._table.delete_item(Key={"item_type": item_type, "item_id": item_id})
            logger.info(f"Deleted {item_type} item: {item_id}")
            return True

        except ClientError as e:
            logger.error(f"DynamoDB error deleting {item_type} item: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting {item_type} item: {str(e)}")
            return False


class OAuthStateStore:
    """Manages OAuth state using DynamoDB."""

    def __init__(self, environment: str, ttl_seconds: int = 600):
        self.ttl_seconds = ttl_seconds
        self._store = DynamoDBStore(environment)

    def store_state(self, state_token: str, provider: str) -> bool:
        """Store OAuth state."""
        return self._store.put_item(
            item_type="oauth_state",
            item_id=state_token,
            data={"provider": provider},
            ttl_seconds=self.ttl_seconds,
        )

    def get_state(self, state_token: str) -> Optional[dict]:
        """Retrieve OAuth state."""
        return self._store.get_item("oauth_state", state_token)

    def delete_state(self, state_token: str) -> bool:
        """Delete OAuth state."""
        return self._store.delete_item("oauth_state", state_token)
