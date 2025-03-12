"""
Configuration settings for the Databricks MCP server.
"""

import os
from typing import Any, Dict, Optional

from dotenv import load_dotenv
from pydantic import BaseSettings, validator

# Load .env file if it exists
load_dotenv()

# Version
VERSION = "0.1.0"


class Settings(BaseSettings):
    """Base settings for the application."""

    # Databricks API configuration
    DATABRICKS_HOST: str
    DATABRICKS_TOKEN: str

    # Server configuration
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8000
    DEBUG: bool = False

    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Version
    VERSION: str = VERSION

    @validator("DATABRICKS_HOST")
    def validate_databricks_host(cls, v: str) -> str:
        """Validate Databricks host URL."""
        if not v.startswith(("https://", "http://")):
            raise ValueError("DATABRICKS_HOST must start with http:// or https://")
        return v

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        case_sensitive = True


# Create global settings instance
settings = Settings()


def get_api_headers() -> Dict[str, str]:
    """Get headers for Databricks API requests."""
    return {
        "Authorization": f"Bearer {settings.DATABRICKS_TOKEN}",
        "Content-Type": "application/json",
    }


def get_databricks_api_url(endpoint: str) -> str:
    """
    Construct the full Databricks API URL.
    
    Args:
        endpoint: The API endpoint path, e.g., "/api/2.0/clusters/list"
    
    Returns:
        Full URL to the Databricks API endpoint
    """
    # Ensure endpoint starts with a slash
    if not endpoint.startswith("/"):
        endpoint = f"/{endpoint}"

    # Remove trailing slash from host if present
    host = settings.DATABRICKS_HOST.rstrip("/")
    
    return f"{host}{endpoint}" 