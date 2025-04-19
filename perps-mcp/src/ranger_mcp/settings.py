from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RangerSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RANGER_", env_file=".env", extra="ignore"
    )

    api_key: str = Field(..., description="API key for Ranger Finance")
    sor_base_url: HttpUrl = Field(..., description="Base URL for the SOR API")
    data_base_url: HttpUrl = Field(...,
                                   description="Base URL for the Data API")


# Load settings once
settings = RangerSettings()
