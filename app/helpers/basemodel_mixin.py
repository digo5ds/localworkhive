from pydantic import BaseModel


class BasemodelMixin(BaseModel):
    """
    Mixin class for Pydantic models that provides utility methods.

    Methods:
        get_null_fields(fields=None):
            Returns a list of field names whose values are currently None.
            Optionally, a subset of fields can be specified to check.
    """

    def get_null_fields(self) -> list:
        """
        Returns a list of field names that are currently None.

        Parameters:
        fields (list): Optional list of field names to consider. If not provided, all fields are considered.

        Returns:
        list: A list of field names that have a value of None.
        """
        fields = dict(self.model_dump().items())
        return [k for k, v in fields.items() if not v]
