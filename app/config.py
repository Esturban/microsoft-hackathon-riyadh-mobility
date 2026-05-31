from functools import lru_cache
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
SAMPLE_DATA_DIR = STATIC_DIR / "sample-data"
DATA_DIR = BASE_DIR / "data"


class Settings(BaseSettings):
    app_name: str = "Riyadh Mobility Intelligence Dashboard"
    app_env: str = "local"
    data_mode: str = "sample"
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    azure_maps_key: str | None = None
    azure_maps_client_id: str | None = None

    azure_storage_account_name: str | None = None
    azure_storage_connection_string: str | None = None
    azure_storage_account_url: str | None = None
    azure_storage_container_raw: str = "raw-data"
    azure_storage_container_processed: str = "processed-data"

    cosmos_endpoint: str | None = None
    cosmos_key: str | None = None
    cosmos_database_name: str = Field(
        default="mobilitydb",
        validation_alias=AliasChoices("COSMOS_DATABASE", "COSMOS_DATABASE_NAME"),
    )
    cosmos_routes_container: str = "routes"
    cosmos_districts_container: str = "districts"
    cosmos_events_container: str = "events"

    event_hub_connection_string: str | None = None
    event_hub_name: str = "mobility-events"

    blob_geojson_prefix: str = ""
    metro_blob_name: str = "metro_lines.geojson"
    bus_blob_name: str = "bus_routes.geojson"
    district_blob_name: str = "district_centers.geojson"
    live_events_blob_name: str = "mock_live_events_sample.json"

    enable_live_events: bool = True
    access_buffer_km: float = 1.5

    sample_metro_file: Path = Field(
        default=SAMPLE_DATA_DIR / "riyadh_metro_lines_sample.geojson"
    )
    sample_bus_file: Path = Field(
        default=SAMPLE_DATA_DIR / "riyadh_bus_routes_sample.geojson"
    )
    sample_district_file: Path = Field(
        default=SAMPLE_DATA_DIR / "district_centers_sample.geojson"
    )
    sample_events_file: Path = Field(
        default=SAMPLE_DATA_DIR / "mock_live_events_sample.json"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
