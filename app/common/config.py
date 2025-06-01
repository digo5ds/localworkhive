"configurations for the application"

from app.__version__ import get_version

lifecyle_policy_template = lifecycle_configuration = {
    "Rules": [
        {
            "ID": "ExpirarArquivosApos1Dias",
            "Filter": {"Prefix": ""},  # Aplica a todos os arquivos
            "Status": "Enabled",
            "Expiration": {"Days": None},
        }
    ]
}
FASTAPI_CONFIG = {
    "title": "Localworkhive API",
    "description": "Api to manage infrastructure data and resources",
    "version": get_version(),
    "license_info": {
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    "openapi_tags": [
        {
            "name": "aws_s3",
            "description": "Operations related to AWS S3 buckets",
        }
    ],
}

API_PORT = 8000
