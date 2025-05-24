from functools import wraps

from botocore.exceptions import (
    ClientError,
    EndpointConnectionError,
    NoCredentialsError,
    PartialCredentialsError,
)


class BotoExceptionHandlingMixin:
    def safe_execute(self, func, *args, **kwargs):
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
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        return self.safe_execute(lambda: method(self, *args, **kwargs))

    return wrapper
