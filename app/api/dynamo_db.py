from datetime import datetime, timezone
from typing import Optional, Dict, Any
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class DynamoDBStore:
    """Generic interface for DynamoDB operations."""

    def __init__(self, table_name: str, partition_key: str = "id"):
        """
        Initialize DynamoDB store.

        Args:
            table_name: Name of DynamoDB table
            partition_key: Name of the partition key (default: 'id')
        """
        self.table_name = table_name
        self.partition_key = partition_key
        self._dynamodb = boto3.resource("dynamodb", region_name="us-west-2")
        self._table = self._dynamodb.Table(table_name)

    def put_item(self, item: Dict[str, Any], ttl_seconds: Optional[int] = None) -> bool:
        """
        Store item in DynamoDB.

        Args:
            item: Dictionary containing item data
            ttl_seconds: Optional TTL in seconds

        Returns:
            bool: True if storage successful
        """
        try:
            if ttl_seconds is not None:
                timestamp = int(datetime.now(timezone.utc).timestamp())
                item["ttl"] = timestamp + ttl_seconds

            self._table.put_item(Item=item)
            logger.info(f"Stored item in table: {self.table_name}")
            return True

        except ClientError as e:
            logger.error(f"DynamoDB error storing item: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error storing item: {str(e)}")
            return False

    def get_item(self, key_value: str, check_ttl: bool = True) -> Optional[dict]:
        """
        Retrieve item from DynamoDB.

        Args:
            key_value: Value of partition key
            check_ttl: Whether to check TTL expiration

        Returns:
            dict: Item data if found and valid
            None: If item not found or invalid
        """
        try:
            response = self._table.get_item(Key={self.partition_key: key_value})

            item = response.get("Item")
            if not item:
                logger.error(f"No item found with key: {key_value}")
                return None

            # Check TTL if required
            if check_ttl and "ttl" in item:
                current_time = int(datetime.now(timezone.utc).timestamp())
                if current_time > item["ttl"]:
                    logger.error(f"Item expired for key: {key_value}")
                    return None

            return item

        except ClientError as e:
            logger.error(f"DynamoDB error retrieving item: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error retrieving item: {str(e)}")
            return None

    def delete_item(self, key_value: str) -> bool:
        """
        Delete item from DynamoDB.

        Args:
            key_value: Value of partition key

        Returns:
            bool: True if deletion successful
        """
        try:
            self._table.delete_item(Key={self.partition_key: key_value})
            logger.info(f"Deleted item with key: {key_value}")
            return True

        except ClientError as e:
            logger.error(f"DynamoDB error deleting item: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting item: {str(e)}")
            return False


class OAuthStateStore:
    """Manages OAuth state using DynamoDB."""

    def __init__(self, environment: str, ttl_seconds: int = 600):
        """Initialize OAuth state storage."""
        self.ttl_seconds = ttl_seconds
        self._store = DynamoDBStore(
            table_name=f"{environment}-oauth-states", partition_key="state"
        )

    def store_state(self, state_token: str, provider: str) -> bool:
        """Store OAuth state."""
        return self._store.put_item(
            item={
                "state": state_token,
                "provider": provider,
                "timestamp": int(datetime.now(timezone.utc).timestamp()),
            },
            ttl_seconds=self.ttl_seconds,
        )

    def get_state(self, state_token: str) -> Optional[dict]:
        """Retrieve OAuth state."""
        return self._store.get_item(state_token)

    def delete_state(self, state_token: str) -> bool:
        """Delete OAuth state."""
        return self._store.delete_item(state_token)
