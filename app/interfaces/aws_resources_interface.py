"""Aws Resources Interface"""

from abc import ABC, abstractmethod
from typing import Optional, Union

from app.helpers.exception_mixin import BotoExceptionHandlingMixin
from app.schemas.aws_resources_basemodels import BucketBaseModel, S3FileStorageModel


class ResourcesInterface(ABC, BotoExceptionHandlingMixin):
    """
    Base interface for managing AWS resources.

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
    def new_resource(self, resource_model: BucketBaseModel | S3FileStorageModel):
        """
        Creates a new AWS S3 resource. The resource must not exist and must be empty.

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
    def delete_resource(self, resource_model: BucketBaseModel | S3FileStorageModel):
        """
        Deletes a AWS S3 resource. The resource must exist and must be empty.

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
        resource_model: BucketBaseModel | S3FileStorageModel | None,
    ):
        """
        Lists the resources of the specified type.

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
    def get_resource(self, resource_model: BucketBaseModel | S3FileStorageModel):
        """
        Gets a AWS S3 resource.

        Parameters:
        resource_model (BucketBaseModel | S3FileStorageModel):
          The model of the resource to be retrieved.

        Returns:
        dict: The metadata of the specified resource.

        Raises:
        botocore.exceptions.ClientError: If the operation fails.
        """
        raise NotImplementedError()
