from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    api_host: str = os.getenv("API_HOST", "0.0.0.0")
    api_port: int = int(os.getenv("API_PORT", "8000"))
    api_version: str = os.getenv("API_VERSION", "v1")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    claude_model: str = "claude-3-5-sonnet-20241022"
    max_ads_per_search: int = int(os.getenv("MAX_ADS_PER_SEARCH", "50"))
    default_country: str = os.getenv("DEFAULT_COUNTRY", "US")
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://localhost:8080"
    ]
    cors_allow_credentials: bool = True
    rate_limit_enabled: bool = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    rate_limit_requests: int = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
    rate_limit_period: int = int(os.getenv("RATE_LIMIT_PERIOD", "60"))
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
