from __future__ import annotations

import os
from pathlib import Path

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobServiceClient


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def get_blob_service_client() -> BlobServiceClient:
    connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
    if connection_string:
        return BlobServiceClient.from_connection_string(connection_string)
    account_url = os.environ["AZURE_STORAGE_ACCOUNT_URL"]
    return BlobServiceClient(account_url=account_url, credential=DefaultAzureCredential())


def upload_dir(directory: Path, container_name: str) -> None:
    client = get_blob_service_client().get_container_client(container_name)
    try:
        client.create_container()
    except Exception:
        pass
    for file_path in directory.glob("*"):
        if not file_path.is_file():
            continue
        with file_path.open("rb") as handle:
            client.upload_blob(file_path.name, handle, overwrite=True)
        print(f"uploaded {container_name}/{file_path.name}")


if __name__ == "__main__":
    upload_dir(RAW_DIR, "raw-data")
    upload_dir(PROCESSED_DIR, "processed-data")
