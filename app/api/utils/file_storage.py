from abc import ABC, abstractmethod
from typing import BinaryIO, Dict, Optional
import boto3
from botocore.exceptions import ClientError
import logging

logger = logging.getLogger(__name__)


class FileStorage(ABC):
    @abstractmethod
    def upload_file(
        self, file_obj: BinaryIO, key: str, content_type: Optional[str] = None
    ) -> str:
        pass

    @abstractmethod
    def start_multipart_upload(
        self, key: str, content_type: Optional[str] = None
    ) -> str:
        pass

    @abstractmethod
    def upload_part(
        self, upload_id: str, key: str, part_number: int, data: bytes
    ) -> Dict:
        pass

    @abstractmethod
    def complete_multipart_upload(self, upload_id: str, key: str, parts: list) -> str:
        pass

    @abstractmethod
    def abort_multipart_upload(self, upload_id: str, key: str) -> None:
        pass


class S3Storage(FileStorage):
    def __init__(self, bucket_name: str):
        self.s3_client = boto3.client("s3")
        self.bucket_name = bucket_name

    def upload_file(
        self, file_obj: BinaryIO, key: str, content_type: Optional[str] = None
    ) -> str:
        extra_args = {"ContentType": content_type} if content_type else {}
        try:
            self.s3_client.upload_fileobj(
                file_obj, self.bucket_name, key, ExtraArgs=extra_args
            )
            return key
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {str(e)}")
            raise

    def start_multipart_upload(
        self, key: str, content_type: Optional[str] = None
    ) -> str:
        try:
            extra_args = {"ContentType": content_type} if content_type else {}
            response = self.s3_client.create_multipart_upload(
                Bucket=self.bucket_name, Key=key, **extra_args
            )
            return response["UploadId"]
        except ClientError as e:
            logger.error(f"Error starting multipart upload: {str(e)}")
            raise

    def upload_part(
        self, upload_id: str, key: str, part_number: int, data: bytes
    ) -> Dict:
        try:
            response = self.s3_client.upload_part(
                Bucket=self.bucket_name,
                Key=key,
                UploadId=upload_id,
                PartNumber=part_number,
                Body=data,
            )
            return {"PartNumber": part_number, "ETag": response["ETag"]}
        except ClientError as e:
            logger.error(f"Error uploading part: {str(e)}")
            raise

    def complete_multipart_upload(self, upload_id: str, key: str, parts: list) -> str:
        try:
            response = self.s3_client.complete_multipart_upload(
                Bucket=self.bucket_name,
                Key=key,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts},
            )
            return response["Location"]
        except ClientError as e:
            logger.error(f"Error completing multipart upload: {str(e)}")
            raise

    def abort_multipart_upload(self, upload_id: str, key: str) -> None:
        try:
            self.s3_client.abort_multipart_upload(
                Bucket=self.bucket_name, Key=key, UploadId=upload_id
            )
        except ClientError as e:
            logger.error(f"Error aborting multipart upload: {str(e)}")
            raise

    def get_presigned_url(self, key: str, expiration: int = 3600) -> str:
        """Generate a presigned URL for accessing an S3 object"""
        try:
            url = self.s3_client.generate_presigned_url(
                "get_object",
                Params={"Bucket": self.bucket, "Key": key},
                ExpiresIn=expiration,
            )
            return url
        except ClientError as e:
            logger.error(f"Error generating presigned URL: {str(e)}")
            return None
