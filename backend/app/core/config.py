# Placeholder for config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AutoModeler"
    API_V1_STR: str = "/api/v1"

    # These will be loaded from your .env file
    NEWS_API_KEY: str
    MLFLOW_TRACKING_URI: str
    GCP_PROJECT_ID: str
    GCP_REGION: str
    GCS_BUCKET_NAME: str

    class Config:
        case_sensitive = True
        env_file = ".env"

# Create an instance of the settings class that the app can import
settings = Settings()