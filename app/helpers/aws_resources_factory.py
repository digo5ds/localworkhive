"""AWS Resource helpers to manage resources."""

import boto3

from app.common.constants import LOCALSTACK_ENDPOINT
from app.helpers.exception_mixin import boto_exceptions_handdler
from app.interfaces.aws_resources_interface import ResourcesInterface
from app.schemas.s3_basemodels import BucketBaseModel


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

    @boto_exceptions_handdler
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

    @boto_exceptions_handdler
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

    @boto_exceptions_handdler
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
            raise ValueError(f"Bucket {resource_model.bucket_name} does not exist.")
        self.s3.delete_bucket(Bucket=resource_model.bucket_name)
        return True

    @boto_exceptions_handdler
    def list_resources(self, resource_model=None) -> list:
        """Lists the buckets in the account.

        Returns:
        list: A list of dictionaries containing the name and creation date of each bucket.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        return self.s3.list_buckets()["Buckets"]
