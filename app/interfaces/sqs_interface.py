"""SQS Interface.

Defines the abstract interface for SQS queue operations, including sending,
receiving, and deleting messages. Classes implementing this interface should
provide concrete implementations for all methods.
"""

from abc import ABC, abstractmethod

from app.helpers.exception_mixin import BotoExceptionHandlingMixin
from app.schemas.aws_resources_basemodels import SQSMessageBaseModel


class SqsInterface(ABC, BotoExceptionHandlingMixin):
    """
    Abstract interface for AWS SQS queue operations.

    This interface enforces the implementation of methods for sending,
    receiving, and deleting messages from an SQS queue. It also includes
    exception handling mixin for consistent error management.
    """

    @abstractmethod
    def send_message(self, resource_model: SQSMessageBaseModel) -> bool:
        """
        Send a message to the specified SQS queue.

        Args:
            resource_model (SQSMessageBaseModel): The model containing the queue URL,
                message body, and optional message attributes.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError()

    @abstractmethod
    def receive_message(self, resource_model: SQSMessageBaseModel) -> list[object]:
        """
        Receive one or more messages from the specified SQS queue.

        Args:
            resource_model (SQSMessageBaseModel): The model containing the queue URL
                and any additional parameters for receiving messages.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError()

    @abstractmethod
    def delete_message(self, resource_model: SQSMessageBaseModel) -> bool:
        """
        Delete a message from the specified SQS queue.

        Args:
            resource_model (SQSMessageBaseModel): The model containing the queue URL
                and the receipt handle of the message to be deleted.

        Raises:
            NotImplementedError: If the method is not implemented by the subclass.
        """
        raise NotImplementedError()
