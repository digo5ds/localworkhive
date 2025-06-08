"""S3 Interface.

Defines the abstract interface for S3 file operations, including creation,
deletion, listing, and reading of files. Classes implementing this interface
should provide concrete implementations for all methods.
"""

from abc import ABC, abstractmethod
from typing import Union

from app.helpers.exception_mixin import BotoExceptionHandlingMixin
from app.schemas.aws_resources_basemodels import S3FileStorageBaseModel


class S3Interface(ABC, BotoExceptionHandlingMixin):
    """
    Abstract interface for AWS S3 file operations.

    This interface enforces the implementation of methods for creating,
    deleting, listing, and reading files from an S3 bucket. It also includes
    exception handling mixin for consistent error management.
    """

    @abstractmethod
    def create_file(self, resource_model: S3FileStorageBaseModel) -> bool:
        """
        Create a file in the specified S3 bucket.

        Args:
            resource_model (S3FileStorageBaseModel): The model containing the bucket name,
                file key, file content, and any additional metadata.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_file(self, resource_model: S3FileStorageBaseModel) -> bool:
        """
        Delete a file from the specified S3 bucket.

        Args:
            resource_model (S3FileStorageBaseModel): The model containing the bucket name
                and file key of the file to be deleted.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError()

    @abstractmethod
    def list_files(self) -> list[object]:
        """
        List all files in the S3 bucket.

        Returns:
            List of file keys.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError()

    @abstractmethod
    def read_file(self, resource_model: S3FileStorageBaseModel) -> Union[str, bytes]:
        """
        Read a file from the specified S3 bucket.

        Args:
            resource_model (S3FileStorageBaseModel): The model containing the bucket name
                and file key of the file to be read.

        Returns:
            The content of the file.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError()
