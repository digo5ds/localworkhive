"""AWS Resources Base Models"""

from typing import Dict, Optional

from pydantic import Field

from app.helpers.basemodel_mixin import BasemodelMixin


class BucketBaseModel(BasemodelMixin):
    """
    Base model for AWS S3 bucket resources.
    """

    name: str = Field(..., description="The name of the S3 bucket.")
    tags: Dict[str, str] = Field(
        default_factory=dict, description="Tags associated with the S3 bucket."
    )
    lifecycle_configuration: Optional[dict] = Field(
        default=None,
        description="Lifecycle configuration for the S3 bucket.",
    )
    bucket_policy: Optional[dict] = Field(
        default=None,
        description="Bucket policy for the S3 bucket.",
    )


class S3FileStorageModel(BasemodelMixin):
    """
    Base model for S3 file storage.
    """

    bucket_name: str = Field(..., description="The name of the S3 bucket.")
    file_key: str = Field(..., description="The key of the file in the S3 bucket.")
    file_content: bytes | None = Field(
        ..., description="The content of the file in bytes."
    )
    metadata: Dict = Field(
        default_factory=dict, description="Metadata associated with the file."
    )

    extra_args: Dict = Field(
        default_factory=dict,
        description="Additional tags associated with the file.",
    )
