import unittest

from pydantic import ValidationError

from app.schemas.s3_basebodels import BucketBaseModel, S3FileStorageBaseModel


class TestBucketBaseModelValidation(unittest.TestCase):
    """Unit tests for the BucketBaseModel validation logic.
    This test class verifies that the BucketBaseModel enforces required fields,
    validates field types, and raises ValidationError when constraints are violated.
    Covers:
    - Successful creation with all required fields.
    - Validation errors when required fields are missing.
    - Validation errors when optional fields are of incorrect type.
    """

    def test_valid_bucket(self):
        """Tests that a valid BucketBaseModel can be created with a required
        bucket_name."""
        model = BucketBaseModel(bucket_name="bucket")
        self.assertEqual(model.bucket_name, "bucket")

    def test_missing_bucket_name(self):
        """Tests that a ValidationError is raised when the bucket_name field is
        missing in the BucketBaseModel."""
        with self.assertRaises(ValidationError):
            BucketBaseModel()

    def test_tags_invalid_type(self):
        """Tests that a ValidationError is raised when the tags field is not a
        dictionary in the BucketBaseModel."""
        with self.assertRaises(ValidationError):
            BucketBaseModel(bucket_name="bucket", tags="not-a-dict")


class TestS3FileStorageBaseModelValidation(unittest.TestCase):
    """Unit tests for the S3FileStorageBaseModel validation logic.

    This test class verifies that the S3FileStorageBaseModel enforces required fields,
    validates field types, and raises ValidationError when constraints are violated.

    Covers:
    - Successful creation with all required fields.
    - Validation errors when required fields.
    - Validation errors when optional fields.
    """

    def test_valid_file(self):
        """
        Tests that a valid S3FileStorageBaseModel can be created with required
        fields: bucket_name, file_key, and file_content.
        """
        model = S3FileStorageBaseModel(
            bucket_name="bucket", file_key="key", file_content=b"abc"
        )
        self.assertEqual(model.bucket_name, "bucket")
        self.assertEqual(model.file_key, "key")
        self.assertEqual(model.file_content, b"abc")

    def test_missing_bucket_name(self):
        """Tests that a ValidationError is raised when the bucket_name field is
        missing in the S3FileStorageBaseModel."""

        with self.assertRaises(ValidationError):
            S3FileStorageBaseModel(file_key="key", file_content=b"abc")

    def test_missing_file_key(self):
        """Tests that a ValidationError is raised when the file_key field is
        missing in the S3FileStorageBaseModel."""

        with self.assertRaises(ValidationError):
            S3FileStorageBaseModel(bucket_name="bucket", file_content=b"abc")

    def test_missing_file_content(self):
        """Tests that a ValidationError is raised when the file_content field
        is missing in the S3FileStorageBaseModel."""
        with self.assertRaises(ValidationError):
            S3FileStorageBaseModel(bucket_name="bucket", file_key="key")

    def test_metadata_invalid_type(self):
        """Tests that a ValidationError is raised when the metadata field is
        not a dictionary in the S3FileStorageBaseModel."""

        with self.assertRaises(ValidationError):
            S3FileStorageBaseModel(
                bucket_name="bucket",
                file_key="key",
                file_content=b"abc",
                metadata="not-a-dict",
            )

    def test_extra_args_invalid_type(self):
        """Tests that providing extra_args with an invalid type raises a
        ValidationError.

        When creating an S3FileStorageBaseModel, the extra_args field
        must be a dictionary. Providing any other type will result in a
        ValidationError.
        """
        with self.assertRaises(ValidationError):
            S3FileStorageBaseModel(
                bucket_name="bucket",
                file_key="key",
                file_content=b"abc",
                extra_args="not-a-dict",
            )


if __name__ == "__main__":
    unittest.main()
