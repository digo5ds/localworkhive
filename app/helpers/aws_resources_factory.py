"""AWS Resource helpers to manage resources."""

from io import BytesIO

import boto3

from app.common.constants import LOCALSTACK_ENDPOINT
from app.helpers.exception_mixin import exception_safe
from app.interfaces.aws_resources_interface import ResourcesInterface
from app.schemas.aws_resources_basemodels import BucketBaseModel, S3FileStorageBaseModel


class BucketS3(ResourcesInterface):
    """BucketS3 provides an interface for managing AWS S3 buckets using boto3,
    supporting operations such as creation, retrieval, deletion, and listing of
    buckets.

    Attributes:
        s3 (boto3.client): The boto3 S3 client configured for the specified region and endpoint.

    Methods:
        __init__(region_name="us-east-1"):
            Initializes the S3 client with the given region and localstack endpoint.

        get_resource(resource_model: BucketBaseModel):
            Retrieves metadata for the specified S3 bucket.

        new_resource(resource_model: BucketBaseModel):
            Creates a new S3 bucket with optional tags and lifecycle configuration.

        delete_resource(resource_model: BucketBaseModel):
            Deletes the specified S3 bucket if it exists.

        list_resources():
            Lists all S3 buckets in the account.

        ValueError: Raised if attempting to create a bucket that already exists
            or delete a bucket that does not exist.
        botocore.exceptions.ClientError: Raised if AWS service operations fail.
    """

    def __init__(self, region_name="us-east-1"):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=LOCALSTACK_ENDPOINT,
            region_name=region_name,
            aws_access_key_id="test",  # Credenciais fictícias
            aws_secret_access_key="test",
        )

    @exception_safe
    def get_resource(self, resource_model: BucketBaseModel):
        """Gets the specified bucket.

        Parameters:
        bucket_name (str): The name of the bucket to be retrieved.

        Returns:
        dict: The metadata of the specified bucket.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        return self.s3.head_bucket(Bucket=resource_model)

    @exception_safe
    def new_resource(self, resource_model: BucketBaseModel):
        """Creates a new S3 bucket based on the provided bucket model.

        Parameters:
        bucket_model (BucketBaseModel):
        The model containing the bucket's details such as
            name, tags,and lifecycle configuration.

        Raises:
        ValueError: If the bucket already exists.

        Exceptions:
        botocore.exceptions.ClientError: If the operation fails due to AWS service issues.
        """

        if resource_model.bucket_name in [
            bucket["Name"] for bucket in self.list_resources()
        ]:
            raise ValueError(f"Bucket {resource_model.bucket_name} already exists.")
        self.s3.create_bucket(Bucket=resource_model.bucket_name)
        if resource_model.lifecycle_configuration:
            self.s3.put_bucket_lifecycle_configuration(
                Bucket=resource_model.bucket_name,
                LifecycleConfiguration=resource_model.lifecycle_configuration,
            )
        if resource_model.tags:
            self.s3.put_bucket_tagging(
                Bucket=resource_model.bucket_name,
                Tagging={
                    "TagSet": [
                        {"Key": key, "Value": value}
                        for key, value in resource_model.tags.items()
                    ]
                },
            )

    @exception_safe
    def delete_resource(self, resource_model: BucketBaseModel):
        """Deletes a S3 bucket.

        Parameters:
        bucket_model (BucketBaseModel):
          The model containing the name of the bucket to be deleted.

        Returns:
        bool: True if the bucket was deleted.

        Raises:
        ValueError: If the bucket does not exist.
        botocore.exceptions.ClientError: If the operation fails.
        """
        if not resource_model.name in [
            bucket["Name"] for bucket in self.list_resources()
        ]:
            raise ValueError(f"Bucket {resource_model.name} does not exist.")
        self.s3.delete_bucket(Bucket=resource_model.name)
        return True

    @exception_safe
    def list_resources(self, resource_model=None) -> list:
        """Lists the buckets in the account.

        Returns:
        list: A list of dictionaries containing the name and creation date of each bucket.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        return self.s3.list_buckets()["Buckets"]


class StorageS3(ResourcesInterface):
    """StorageS3 provides an interface for interacting with AWS S3 storage
    buckets.

    This class implements methods to upload, delete, list, and retrieve files from an S3 bucket,
    using the boto3 client. It is designed to work with a specified bucket and region, and can
    optionally use a custom endpoint (e.g., for localstack).

    Attributes:
        s3 (boto3.client): The boto3 S3 client instance.
    Methods:
        new_resource(resource_model: S3FileStorageModel):
            Uploads a file to the specified S3 bucket.

        delete_resource(resource_model: S3FileStorageModel):
            Deletes a file from the specified S3 bucket.

        list_resources(resource_model: S3FileStorageModel):
            Lists all objects in the specified S3 bucket.

        get_resource(resource_model: S3FileStorageModel):
            Downloads and returns the contents of a file from the specified S3 bucket.
    """

    def __init__(self, region_name="us-east-1"):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=LOCALSTACK_ENDPOINT,
            region_name=region_name,
        )

    @exception_safe
    def new_resource(self, resource_model: S3FileStorageBaseModel):
        """Uploads a file to the specified bucket.

        Parameters:
        file_name (str): The name to be given to the uploaded file.
        file_path (str): The path to the local file to be uploaded.

        Returns:
        str: A message indicating the status of the operation.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """

        with BytesIO(resource_model.file_content) as file_content:
            file_content.seek(0)  # Reset the file pointer to the beginning
            self.s3.upload_fileobj(
                Fileobj=file_content,
                Key=resource_model.file_key,
                Bucket=resource_model.bucket_name,
                ExtraArgs=resource_model.extra_args,
            )

    @exception_safe
    def delete_resource(
        self, resource_model: S3FileStorageBaseModel
    ) -> S3FileStorageBaseModel:
        """Deletes the specified file from the specified bucket.

        Parameters:
        file_name (str): The name of the file to be deleted.

        Returns:
        str: A message indicating the status of the operation.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        return self.s3.delete_object(
            Bucket=resource_model.bucket_name, Key=resource_model.file_key
        )

    @exception_safe
    def list_resources(self, resource_model: S3FileStorageBaseModel):
        """Lists all the objects in the specified bucket.

        Returns:
        list: A list of keys representing the objects in the bucket. If
            the bucket is empty, an empty list is returned.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        files = []
        response = self.s3.list_objects_v2(Bucket=resource_model.bucket_name)
        if "Contents" in response:
            for obj in response["Contents"]:
                files.append(
                    S3FileStorageBaseModel(
                        bucket_name=resource_model.bucket_name,
                        file_key=obj["Key"],
                        file_content=None,  # Content is not needed for listing
                        extra_args=self.s3.head_object(
                            Bucket=resource_model.bucket_name,
                            Key=resource_model.file_key,
                        )["Metadata"],
                        metadata={
                            "LastModified": obj["LastModified"].isoformat(),
                            "Size": obj["Size"],
                            "ETag": obj["ETag"].strip('"'),
                        },
                    )
                )

        return files

    @exception_safe
    def get_resource(self, resource_model: S3FileStorageBaseModel):
        """Downloads the specified file from the specified bucket.

        Parameters:
        file_name (str): The name of the file to be downloaded.

        Returns:
        str: The contents of the file as a string.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        response = self.s3.get_object(
            Bucket=resource_model.bucket_name, Key=S3FileStorageBaseModel.file_key
        )
        return response["Body"].read().decode("utf-8")
