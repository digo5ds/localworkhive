"""
This module provides utilities for handling
common exceptions when interacting with AWS services using boto3/botocore.
"""

from functools import wraps

from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
    NoCredentialsError,
    PartialCredentialsError,
)


class BotoExceptionHandlingMixin:
    """
    A mixin class that provides a method to safely execute
    functions interacting with AWS services,
    handling common boto3 exceptions.
    """

    def safe_execute(self, func, *args, **kwargs):
        """
        Executes a function safely by catching and handling specific
        AWS-related exceptions.

        This method attempts to execute the provided
        function with the given arguments and keyword arguments.
        If an exception of type ClientError, EndpointConnectionError,
        NoCredentialsError, orPartialCredentialsError
        is raised during execution, it is caught, logged, and re-raised.

        Parameters:
        func (callable): The function to be executed.
        args: Positional arguments to be passed to the function.
        kwargs: Keyword arguments to be passed to the function.

        Returns:
        The result of the function call if no exceptions are raised.

        Raises:
        ClientError, EndpointConnectionError,
        NoCredentialsError, PartialCredentialsError:
        If one of these exceptions occurs during function execution,
        it is caught, logged, and re-raised.
        """

        try:
            return func(*args, **kwargs)
        except (
            ClientError,
            EndpointConnectionError,
            NoCredentialsError,
            PartialCredentialsError,
        ) as e:
            print(f"[ERROR]: {type(e).__name__} - {str(e)}")
            raise e


def exception_safe(method):
    """
    Decorator to wrap a method in safe_execute to catch and handle exceptions.

    The wrapper calls the wrapped method with the provided arguments and keyword arguments,
    and catches any exceptions of type ClientError, EndpointConnectionError, NoCredentialsError,
    and PartialCredentialsError. If an exception is caught, it is printed to the console and
    re-raised.

    :param self: The instance of the class containing the wrapped method.
    :param args: The positional arguments to be passed to the wrapped method.
    :param kwargs: The keyword arguments to be passed to the wrapped method.
    :return: The result of calling the wrapped method, or None if an exception was caught.
    """

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        return self.safe_execute(lambda: method(self, *args, **kwargs))

    return wrapper
