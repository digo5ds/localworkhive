from fastapi import APIRouter, Depends, HTTPException

from app.helpers.aws_resources_factory import BucketS3, StorageS3
from app.schemas.aws_resources_basemodels import BucketBaseModel, S3FileStorageModel

router = APIRouter(prefix="/aws")


def get_bucket_helper() -> BucketS3:
    """
    Helper function to return a BucketS3 instance.

    Returns:
        BucketS3: An instance of the BucketS3 class for managing S3 buckets.
    """
    return BucketS3()


def get_s3_storage_helper() -> StorageS3:
    """
    Helper function to return a StorageS3 instance.

    Returns:
        StorageS3: An instance of the StorageS3 class for managing S3 file storage.
    """
    return StorageS3()


@router.put("/s3/upload")
def upload_file(
    file_data: S3FileStorageModel, s3_storage_helper=Depends(get_s3_storage_helper)
):
    """
    Uploads a file to AWS S3.

    Args:
    file (S3FileStorageModel): The file to be uploaded.
    bucket_name (str): The name of the bucket to upload the file to.
    file_key (str): The key of the file in the bucket.
    file_content (bytes): The content of the file in bytes.

    Returns:
    dict: A dictionary containing a message indicating the status of the operation.

    Raises:
    HTTPException: If the operation fails.
    """
    try:
        empty_mandatory_fields = file_data.get_null_fields()
        if not any(
            item in ["bucket_name", "file_key", "file_content"]
            for item in empty_mandatory_fields
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Mandatory fields are missing: {empty_mandatory_fields}",
            )
        s3_storage_helper.new_resource(file_data)
        return {"message": "File uploaded successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.delete("/s3/delete")
def delete_file(
    file_data: S3FileStorageModel, s3_storage_helper=Depends(get_s3_storage_helper)
):
    """
    Uploads a file to AWS S3.

    Args:
    file (S3FileStorageModel): The file to be uploaded.
    bucket_name (str): The name of the bucket to upload the file to.
    file_key (str): The key of the file in the bucket.
    file_content (bytes): The content of the file in bytes.

    Returns:
    dict: A dictionary containing a message indicating the status of the operation.

    Raises:
    HTTPException: If the operation fails.
    """
    try:
        empty_mandatory_fields = file_data.get_null_fields()
        if any(item in ["bucket_name", "file_key"] for item in empty_mandatory_fields):
            raise HTTPException(
                status_code=400,
                detail=f"Mandatory fields are missing: {empty_mandatory_fields}",
            )
        return {
            "message": "File removed successfully",
            "deleted_file": s3_storage_helper.delete_resource(file_data),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


@router.get("/s3/read/{file_data.bucket_name}/{file_data.file_key}")
def get_file(
    file_data: S3FileStorageModel, s3_storage_helper=Depends(get_s3_storage_helper)
):
    """
    Retrieves a file from AWS S3.

    Args:
    file (S3FileStorageModel): The file to be retrieved.
    bucket_name (str): The name of the bucket to retrieve the file from.
    file_key (str): The key of the file in the bucket.

    Returns:
    dict: A dictionary containing a message indicating the status of the operation.

    Raises:
    HTTPException: If the operation fails.
    """
    try:
        empty_mandatory_fields = file_data.get_null_fields()
        if not all(
            item in ["bucket_name", "file_key"] for item in empty_mandatory_fields
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Mandatory fields are missing: {empty_mandatory_fields}",
            )
        return s3_storage_helper.get_resource(file_data)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def list_files(
    file_data: BucketBaseModel, s3_storage_helper=Depends(get_s3_storage_helper)
):
    """
    Retrieves a bucket from AWS S3.

    Args:
    """
    try:
        empty_mandatory_fields = file_data.get_null_fields()
        if not all(item in ["nbucket_nameame"] for item in empty_mandatory_fields):
            raise HTTPException(
                status_code=400,
                detail=f"Mandatory fields are missing: {empty_mandatory_fields}",
            )
        s3_storage_helper.get_resource(file_data)
        return {"message": "File removed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def create_bucket(
    bucket_data: BucketBaseModel, s3_bucket_helper=Depends(get_bucket_helper)
):
    """
    Creates a bucket in AWS S3.

    Args:
    bucket_data (BucketBaseModel): The data for the bucket to be created.

    Returns:
    dict: A dictionary containing a message indicating the status of the operation.

    Raises:
    HTTPException: If the operation fails.
    """
    try:
        s3_bucket_helper.new_resource(bucket_data)
        return {"message": "Bucket created successfully", "bucket_data": bucket_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def delete_bucket(
    bucket_data: BucketBaseModel, s3_bucket_helper=Depends(get_bucket_helper)
):
    """
    Deletes a bucket in AWS S3.

    Args:
    bucket_data (BucketBaseModel): The data for the bucket to be deleted.

    Returns:
    dict: A dictionary containing a message indicating the status of the operation.

    Raises:
    HTTPException: If the operation fails.
    """
    try:
        s3_bucket_helper.delete_resource(bucket_data)
        return {"message": "Bucket deleted successfully", bucket_data: bucket_data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def get_bucket(
    bucket_data: BucketBaseModel, s3_bucket_helper=Depends(get_bucket_helper)
):
    """
    Retrieves a bucket from AWS S3.

    Args:
    bucket_data (BucketBaseModel): The data for the bucket to be retrieved.

    Returns:
    dict: A dictionary containing the metadata of the specified bucket.

    Raises:
    HTTPException: If the operation fails.
    """
    try:
        return s3_bucket_helper.get_resource(bucket_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


def list_buckets(s3_bucket_helper=Depends(get_bucket_helper)):
    """
    Lists all buckets in AWS S3.

    Returns:
    dict: A dictionary containing a list of all buckets.

    Raises:
    HTTPException: If the operation fails.
    """
    try:
        return s3_bucket_helper.list_resources()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
