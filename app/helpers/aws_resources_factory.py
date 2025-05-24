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
        self.s3.head_bucket(Bucket=bucket_name)

    @exception_safe
    def new_resource(self, bucket_name):
        if bucket_name in [bucket["Name"] for bucket in self.list_resources()]:
            raise ValueError(f"Bucket {bucket_name} already exists.")
        self.s3.create_bucket(Bucket=bucket_name)

    @exception_safe
    def delete_resource(self, bucket_name):
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
        self.s3.upload_file(file_path, self.bucket_name, file_name)
        return f"File {file_name} uploaded to bucket {self.bucket_name}."

    @exception_safe
    def delete_resource(self, file_name):
        self.s3.delete_object(Bucket=self.bucket_name, Key=file_name)
        return f"File {file_name} deleted from bucket {self.bucket_name}."

    @exception_safe
    @exception_safe
    def list_resources(self):
        response = self.s3.list_objects_v2(Bucket=self.bucket_name)
        if "Contents" in response:
            return [obj["Key"] for obj in response["Contents"]]
        else:
            return []

    @exception_safe
    def get_resource(self, file_name):
        response = self.s3.get_object(Bucket=self.bucket_name, Key=file_name)
        return response["Body"].read().decode("utf-8")
