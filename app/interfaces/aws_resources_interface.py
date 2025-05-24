from abc import ABC, abstractmethod

from app.helpers.exception_mixin import BotoExceptionHandlingMixin


class ResourcesInterface(ABC, BotoExceptionHandlingMixin):
    @abstractmethod
    def new_resource(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete_resource(self, resource_name):

        pass

    @abstractmethod
    def list_resources(self, resource_name):
        pass

    @abstractmethod
    def get_resource(self, resource_name):
        pass
