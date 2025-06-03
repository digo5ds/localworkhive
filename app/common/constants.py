"""
This module contains constants used throughout the application.
"""

import os

LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
