import boto3

from app.common.constants import LOCALSTACK_ENDPOINT
from app.helpers.exception_mixin import exception_safe
from app.interfaces.aws_resources_interface import ResourcesInterface


class BucketS3(ResourcesInterface):
    def __init__(self, region_name="us-east-1"):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=LOCALSTACK_ENDPOINT,
            region_name=region_name,
            aws_access_key_id="test",  # Credenciais fictícias
            aws_secret_access_key="test",
        )

    @exception_safe
    def get_resource(self, bucket_name):
        """
        Gets the specified bucket.

        Parameters:
        bucket_name (str): The name of the bucket to be retrieved.

        Returns:
        dict: The metadata of the specified bucket.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        return self.s3.head_bucket(Bucket=bucket_name)

    @exception_safe
    def new_resource(self, bucket_name):
        """
        Creates the specified bucket. The bucket must not exist and must be empty.

        Parameters:
        bucket_name (str): The name of the bucket to be created.

        Returns:
        bool: True if the bucket was created.

        Raises:
        ValueError: If the bucket already exists or if the bucket is not empty.
        """
        if bucket_name in [bucket["Name"] for bucket in self.list_resources()]:
            raise ValueError(f"Bucket {bucket_name} already exists.")
        self.s3.create_bucket(Bucket=bucket_name)

    @exception_safe
    def delete_resource(self, bucket_name):
        """
        Deletes the specified bucket. The bucket must exist and must be empty.
        It will raise a ValueError if the bucket does not exist or if the bucket is not empty.

        Parameters:
        bucket_name (str): The name of the bucket to be deleted.

        Returns:
        bool: True if the bucket was deleted.

        Raises:
        ValueError: If the bucket does not exist or if the bucket is not empty.
        """
        if not bucket_name in [bucket["Name"] for bucket in self.list_resources()]:
            raise ValueError(f"Bucket {bucket_name} does not exist.")
        self.s3.delete_bucket(Bucket=bucket_name)
        return True

    @exception_safe
    def list_resources(self):
        response = self.s3.list_buckets()
        return [bucket for bucket in response["Buckets"]]


class StorageS3(ResourcesInterface):
    def __init__(self, bucket_name, region_name="us-east-1"):
        self.s3 = boto3.client(
            "s3",
            endpoint_url=LOCALSTACK_ENDPOINT,
            region_name=region_name,
        )
        self.bucket_name = bucket_name

    @exception_safe
    def new_resource(self, file_name, file_path):
        """
        Uploads a file to the specified bucket.

        Parameters:
        file_name (str): The name to be given to the uploaded file.
        file_path (str): The path to the local file to be uploaded.

        Returns:
        str: A message indicating the status of the operation.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        self.s3.upload_file(file_path, self.bucket_name, file_name)
        return f"File {file_name} uploaded to bucket {self.bucket_name}."

    @exception_safe
    def delete_resource(self, file_name):
        """
        Deletes the specified file from the specified bucket.

        Parameters:
        file_name (str): The name of the file to be deleted.

        Returns:
        str: A message indicating the status of the operation.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)
        return f"File {file_name} deleted from bucket {self.bucket_name}."

    @exception_safe
    def list_resources(self):
        """
        Lists all the objects in the specified bucket.

        Returns:
        list: A list of keys representing the objects in the bucket. If
            the bucket is empty, an empty list is returned.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """

        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        if "Contents" in response:
            return [obj["Key"] for obj in response["Contents"]]
        else:
            return []

    @exception_safe
    def get_resource(self, file_name):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=file_name)
        return response["Body"].read().decode("utf-8")
