"""Aws Services Routes."""

from fastapi import APIRouter, Depends, HTTPException

from app.helpers.api_validator_helper import required_fields_is_filled
from app.helpers.aws_resources_factory import BucketS3, StorageS3
from app.schemas.aws_resources_basemodels import BucketBaseModel, S3FileStorageBaseModel

router = APIRouter(prefix="/aws/s3")


def __get_bucket_helper() -> BucketS3:
    """Helper function to return a BucketS3 instance.

    Returns:
        BucketS3: An instance of the BucketS3 class for managing S3 buckets.
    """
    return BucketS3()


def __get_s3_storage_helper() -> StorageS3:
    """Helper function to return a StorageS3 instance.

    Returns:
        StorageS3: An instance of the StorageS3 class for managing S3 file storage.
    """
    return StorageS3()


@router.put("/upload_file")
def upload_file(
    file_data: S3FileStorageBaseModel,
    s3_storage_helper=Depends(__get_s3_storage_helper),
):
    """Uploads a file to AWS S3.

    Args:
    file_data (S3FileStorageModel): The data for the file to be uploaded, including
    bucket name, file key, and file content.

    Returns:
    dict: A dictionary containing a message indicating the success of the upload operation.

    Raises:
    HTTPException: If the operation fails or mandatory fields are missing.
    """

    try:
        validation_result = required_fields_is_filled(
            ["bucket_name", "file_key", "file_content"], file_data
        )
        if validation_result:
            s3_storage_helper.new_resource(file_data)
            return {"message": "File uploaded successfully"}

        raise HTTPException(
            status_code=400,
            detail=f"Mandatory fields are missing: {validation_result}",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/s3/delete")
def delete_file(
    file_data: S3FileStorageBaseModel,
    s3_storage_helper=Depends(__get_s3_storage_helper),
):
    """Deletes a file from AWS S3.

    Args:
    file_data (S3FileStorageModel): The data for the file to be deleted, including
    bucket name and file key.

    Returns:
    dict: A dictionary containing a message indicating the status of the operation.

    Raises:
    HTTPException: If the operation fails.
    """
    try:
        validation_result = required_fields_is_filled(
            ["bucket_name", "file_key"], file_data
        )
        if validation_result is True:
            return {
                "message": "File removed successfully",
                "deleted_file": s3_storage_helper.delete_resource(file_data),
            }
        raise HTTPException(
            status_code=400,
            detail=f"Mandatory fields are missing: {validation_result}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/s3/read/{file_data.bucket_name}/{file_data.file_key}")
def get_file(
    file_data: S3FileStorageBaseModel,
    s3_storage_helper=Depends(__get_s3_storage_helper),
):
    """Retrieves a file from AWS S3.

    Args:
    file_data (S3FileStorageModel): The data for the file to be retrieved, including
    bucket name and file key.

    Returns:
    str: The contents of the file if retrieval is successful.

    Raises:
    HTTPException: If mandatory fields are missing or if the operation fails.
    """

    try:
        validation_result = required_fields_is_filled(
            ["bucket_name", "file_key"], file_data
        )
        if validation_result is True:
            return s3_storage_helper.get_resource(file_data)
        raise HTTPException(
            status_code=400,
            detail=f"Mandatory fields are missing: {validation_result}",
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/s3/list/{file_data.bucket_name}")
def list_files(
    file_data: BucketBaseModel, s3_storage_helper=Depends(__get_s3_storage_helper)
):
    """Retrieves a bucket from AWS S3.

    Args:
    """
    try:
        validation_result = required_fields_is_filled(["bucket_name"], file_data)
        if validation_result is True:
            s3_storage_helper.get_resource(file_data)
        raise HTTPException(
            status_code=400,
            detail=f"Mandatory fields are missing: {validation_result}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.post("/create_bucket")
def create_bucket(
    bucket_data: BucketBaseModel, s3_bucket_helper=Depends(__get_bucket_helper)
):
    """Creates a bucket in AWS S3.
    Warning: The Field `bucket_name` is mandatory for this operation.

    Args:
    bucket_data (BucketBaseModel): The data for the bucket to be created.

    Returns:
    dict: A dictionary containing a message indicating the status of the operation.

    Raises:
    HTTPException: If the operation fails.
    """

    validation_result = required_fields_is_filled(["bucket_name"], bucket_data)
    if validation_result is True:
        try:
            s3_bucket_helper.new_resource(bucket_data)
            return {
                "message": "Bucket created successfully",
                "bucket_data": bucket_data,
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e)) from e

    raise HTTPException(
        status_code=400,
        detail=f"Mandatory fields are missing: {validation_result}",
    )


@router.delete("/delete_bucket")
def delete_bucket(
    bucket_data: BucketBaseModel, s3_bucket_helper=Depends(__get_bucket_helper)
):
    """Deletes a bucket in AWS S3.
    Warning: The Field `bucket_name` is mandatory for this operation.    Args:
        bucket_data (BucketBaseModel): The data for the bucket to be deleted.

        Returns:
        dict: A dictionary containing a message indicating the status of the operation.

        Raises:
        HTTPException: If the operation fails.
    """
    try:
        validation_result = required_fields_is_filled(["bucket_name"], bucket_data)
        if validation_result is True:
            s3_bucket_helper.delete_resource(bucket_data)
            return {
                "message": "Bucket deleted successfully",
                "bucket_data": bucket_data,
            }
        raise HTTPException(
            status_code=400,
            detail=f"Mandatory fields are missing: {validation_result}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/get_bucket{bucket_data.bucket_name}")
def get_bucket(
    bucket_data: BucketBaseModel, s3_bucket_helper=Depends(__get_bucket_helper)
):
    """Retrieves a bucket from AWS S3.
    Warning: The Field `bucket_name` is mandatory for this operation.
    Args:
    bucket_data (BucketBaseModel): The data for the bucket to be retrieved.

    Returns:
    dict: A dictionary containing the metadata of the specified bucket.

    Raises:
    HTTPException: If the operation fails.
    """
    try:
        validation_result = required_fields_is_filled(["bucket_name"], bucket_data)
        if validation_result is True:
            # Assuming get_resource returns the bucket metadata
            return s3_bucket_helper.get_resource(bucket_data)
        raise HTTPException(
            status_code=400,
            detail=f"Mandatory fields are missing: {validation_result}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/list_buckets")
def list_buckets(s3_bucket_helper=Depends(__get_bucket_helper)):
    """Lists all buckets in AWS S3.

    Returns:
    dict: A dictionary containing a list of all buckets.

    Raises:
    HTTPException: If the operation fails.
    """
    try:
        return s3_bucket_helper.list_resources()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
