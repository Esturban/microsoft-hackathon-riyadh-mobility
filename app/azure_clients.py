from __future__ import annotations

from functools import lru_cache

from .config import get_settings


try:
    from azure.cosmos import CosmosClient
except ImportError:  # pragma: no cover - optional dependency at runtime
    CosmosClient = None

try:
    from azure.identity import DefaultAzureCredential
    from azure.storage.blob import BlobServiceClient
except ImportError:  # pragma: no cover - optional dependency at runtime
    BlobServiceClient = None
    DefaultAzureCredential = None


@lru_cache
def get_blob_service_client():
    settings = get_settings()
    if BlobServiceClient is None:
        return None
    if settings.azure_storage_connection_string:
        return BlobServiceClient.from_connection_string(
            settings.azure_storage_connection_string
        )
    if settings.azure_storage_account_url and DefaultAzureCredential is not None:
        return BlobServiceClient(
            account_url=settings.azure_storage_account_url,
            credential=DefaultAzureCredential(),
        )
    return None


@lru_cache
def get_cosmos_database_client():
    settings = get_settings()
    if CosmosClient is None or not settings.cosmos_endpoint:
        return None

    credential = settings.cosmos_key or (
        DefaultAzureCredential() if DefaultAzureCredential is not None else None
    )
    if credential is None:
        return None

    client = CosmosClient(settings.cosmos_endpoint, credential=credential)
    return client.get_database_client(settings.cosmos_database_name)
