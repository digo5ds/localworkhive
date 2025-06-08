"""Unit tests for AWS services routes in the application."""

import unittest
from unittest.mock import MagicMock, patch

from app.routes import s3_routes
from app.schemas.aws_resources_basemodels import BucketBaseModel, S3FileStorageBaseModel


class TestAwsServicesRoutes(unittest.TestCase):
    """Unit tests for AWS services routes.

    Covers:
    - File upload and deletion
    - Bucket creation and deletion
    - Field validation handling
    - Interaction with helper classes (mocked)
    """

    @patch("app.routes.s3_routes.required_fields_is_filled")
    def test_upload_file_success(self, mock_validation_result):
        """Tests that the upload_file endpoint returns a success message and
        calls the 'create_file' method of the given S3StorageHelper when all
        mandatory fields are present."""
        mock_helper = MagicMock()
        file_data = S3FileStorageBaseModel(
            bucket_name="bucket", file_key="key", file_content=b"content"
        )
        mock_validation_result.return_value = True
        response = s3_routes.upload_file(file_data, s3_storage_helper=mock_helper)
        self.assertEqual(response, {"message": "File uploaded successfully"})
        mock_helper.create_file.assert_called_once_with(file_data)

    @patch("app.routes.s3_routes.required_fields_is_filled")
    def test_delete_file_success(self, mock_validation_result):
        """Tests that the delete_file endpoint returns a success message and
        calls the 'delete_file' method of the given S3StorageHelper when
        all mandatory fields are present."""
        mock_helper = MagicMock()
        file_data = S3FileStorageBaseModel(
            bucket_name="bucket", file_key="key", file_content=b"content"
        )
        mock_validation_result.return_value = True
        mock_helper.delete_file.return_value = True
        response = s3_routes.delete_file(file_data, s3_storage_helper=mock_helper)
        self.assertEqual(response["message"], "File removed successfully")
        mock_helper.delete_file.assert_called_once_with(file_data)

    @patch("app.routes.s3_routes.required_fields_is_filled")
    def test_create_bucket_success(self, mock_validation_result):
        """Tests that the create_bucket endpoint returns a success message and
        calls the 'new_resource' method of the given S3BucketHelper when all
        mandatory fields are present."""
        mock_helper = MagicMock()
        bucket_data = BucketBaseModel(bucket_name="bucket")
        mock_validation_result.return_value = True
        response = s3_routes.create_bucket(bucket_data, s3_bucket_helper=mock_helper)
        self.assertEqual(response["message"], "Bucket created successfully")
        mock_helper.new_resource.assert_called_once_with(bucket_data)

    @patch("app.routes.s3_routes.required_fields_is_filled")
    def test_delete_bucket_success(self, mock_validation_result):
        """Tests that the delete_bucket endpoint returns a success message and
        calls the 'delete_resource' method of the given S3BucketHelper when all
        mandatory fields are present."""
        mock_helper = MagicMock()
        bucket_data = BucketBaseModel(bucket_name="bucket")
        mock_validation_result.return_value = True
        response = s3_routes.delete_bucket(bucket_data, s3_bucket_helper=mock_helper)
        self.assertEqual(response["message"], "Bucket deleted successfully")
        mock_helper.delete_resource.assert_called_once_with(bucket_data)


if __name__ == "__main__":
    unittest.main()
