"""AWS Resources Base Models."""

from typing import Dict, Literal, Optional

from pydantic import Field, constr

from app.helpers.basemodel_mixin import BasemodelMixin

ACLType = constr(
    pattern=r"^(private|public-read|public-read-write|authenticated-read)$"
)


class BucketBaseModel(BasemodelMixin):
    """Base model for AWS S3 bucket resources."""

    bucket_name: str = Field(..., description="The name of the S3 bucket.")
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


class S3ExtraArgs(BasemodelMixin):
    """Extra arguments for S3 upload."""

    # Usando Literal para restringir os valores possíveis de ACL
    ACL: Optional[
        Literal["private", "public-read", "public-read-write", "authenticated-read"]
    ] = None

    # Metadata: Dicionário de metadados
    Metadata: Optional[Dict[str, str]] = None

    # ContentType: O tipo do conteúdo do arquivo
    ContentType: Optional[str] = None

    # Outros campos que você possa querer adicionar, como "ServerSideEncryption", "StorageClass", etc.
    ServerSideEncryption: Optional[str] = None
    StorageClass: Optional[str] = None

    # Exemplo de tag
    Tagging: Optional[str] = None


class S3FileStorageBaseModel(BasemodelMixin):
    """Base model for S3 file storage."""

    model_config = {"extra": "allow"}
    bucket_name: str = Field(..., description="The name of the S3 bucket.")
    file_key: str = Field(..., description="The key of the file in the S3 bucket.")
    file_content: Optional[bytes] = Field(
        ..., description="The content of the file in bytes."
    )
    # Argumentos extras, incluindo ACL, ContentType, Metadata, etc.
    extra_args: Optional[S3ExtraArgs] = Field(
        default=None,
        description="Additional tags and parameters associated with the file.",
    )
