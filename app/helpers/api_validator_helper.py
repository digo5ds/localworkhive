from fastapi import APIRouter, HTTPException

from app.schemas.aws_resources_basemodels import BucketBaseModel, S3FileStorageBaseModel


def required_fields_is_filled(
    required_fields: list, model: S3FileStorageBaseModel | BucketBaseModel
):
    """Validates if all the mandatory fields are provided in the model.

    Args:
        required_fields (list): The list of required fields.
        model (S3FileStorageModel | BucketBaseModel): The model containing the data.

    Returns:
        bool: True if all fields are provided, False otherwise.

    Raises:
        HTTPException: If any required field is missing.
    """
    missing_fields = [f for f in required_fields if f in model.get_null_fields()]
    if missing_fields:
        return missing_fields
    return True
