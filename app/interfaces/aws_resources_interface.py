"""Aws Resources Interface."""

from abc import ABC, abstractmethod

from app.helpers.exception_mixin import BotoExceptionHandlingMixin
from app.schemas.aws_resources_basemodels import BucketBaseModel, S3FileStorageBaseModel


class ResourcesInterface(ABC, BotoExceptionHandlingMixin):
    """Base interface for managing AWS resources.

    This class defines abstract methods that must be implemented
    by any resource class interacting with AWS services. It enforces
    a consistent interface for resource creation, retrieval, and deletion,
    along with standardized exception handling through BotoExceptionHandlingMixin.

    Inherits:
        ABC: For defining abstract base classes.
        BotoExceptionHandlingMixin: For handling Boto3-related exceptions.

    Abstract methods:
        new_resource: Create a new AWS resource.
        delete_resource: Delete a specific AWS resource.
        get_resources: Retrieve resources.
        delete_resources: Delete AWS resources.
    """

    @abstractmethod
    def new_resource(self, resource_model: BucketBaseModel | S3FileStorageBaseModel):
        """Creates a new AWS S3 resource. The resource must not exist and must
        be empty.

        Parameters:
        resource_model (BucketBaseModel | S3FileStorageModel):
            The model of the resource to be created.

        Returns:
        bool: True if the resource was created.

        Raises:
        ValueError: If the resource already exists or if the resource is not empty.
        """

        raise NotImplementedError()

    @abstractmethod
    def delete_resource(self, resource_model: BucketBaseModel | S3FileStorageBaseModel):
        """Deletes a AWS S3 resource. The resource must exist and must be
        empty.

        Parameters:
        resource_model (BucketBaseModel | S3FileStorageModel):
            The model of the resource to be deleted.

        Returns:
        bool: True if the resource was deleted.

        Raises:
        ValueError: If the resource does not exist or if the resource is not empty.
        """
        raise NotImplementedError()

    @abstractmethod
    def list_resources(
        self,
        resource_model: BucketBaseModel | S3FileStorageBaseModel | None,
    ):
        """Lists the resources of the specified type.

        Parameters:
        resource_model (BucketBaseModel | S3FileStorageModel):
            The model of the resource to be listed.

        Returns:
        list: A list of resource models.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        raise NotImplementedError()

    @abstractmethod
    def get_resource(self, resource_model: BucketBaseModel | S3FileStorageBaseModel):
        """Gets a AWS S3 resource.

        Parameters:
        resource_model (BucketBaseModel | S3FileStorageModel):
          The model of the resource to be retrieved.

        Returns:
        dict: The metadata of the specified resource.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        raise NotImplementedError()


class SqsInterface(ABC, BotoExceptionHandlingMixin):
    """Base interface for managing AWS resources.

    This class defines abstract methods that must be implemented
    by any resource class interacting with AWS services. It enforces
    a consistent interface for resource creation, retrieval, and deletion,
    along with standardized exception handling through BotoExceptionHandlingMixin.

    Inherits:
        ABC: For defining abstract base classes.
        BotoExceptionHandlingMixin: For handling Boto3-related exceptions.

    Abstract methods:
        new_resource: Create a new AWS resource.
        delete_resource: Delete a specific AWS resource.
        get_resources: Retrieve resources.
        delete_resources: Delete AWS resources.
    """

    @abstractmethod
    def send_message(self, resource_model):
        """Creates a new AWS SQS resource.

        Parameters:
        resource_model: The model of the resource to be created.

        Returns:
        str: The URL of the created SQS queue.

        Raises:
        ValueError: If the resource already exists.
        botocore.exceptions.ClientError: If the operation fails.
        """
        raise NotImplementedError()

    @abstractmethod
    def receive_message(self, resource_model):
        """Receives messages from an AWS SQS queue.

        Parameters:
        resource_model: The model of the resource to be received.

        Returns:
        dict: The received messages.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_message(self, resource_model):
        """Deletes a message from an AWS SQS queue.

        Parameters:
        resource_model: The model of the resource to be deleted.

        Returns:
        bool: True if the message was deleted.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        raise NotImplementedError()
