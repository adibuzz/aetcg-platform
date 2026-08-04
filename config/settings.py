import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class AppSettings(BaseSettings):
    APP_ENV: str = os.getenv("APP_ENV", "development")
    API_PORT: int = int(os.getenv("API_PORT", 8000))
    REDIS_HOST: str = os.getenv("REDIS_HOST", "localhost")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", 6379))
    EXTERNAL_COMPLIANCE_API_URL: str = os.getenv(
        "EXTERNAL_COMPLIANCE_API_URL", "https://api.mockcompliance.org/v1/validate"
    )
    EXTERNAL_API_TIMEOUT_SEC: float = float(os.getenv("EXTERNAL_API_TIMEOUT_SEC", 5.0))

    LLM_ENDPOINT_URL: str = os.getenv("LLM_ENDPOINT_URL", "https://studio.bearcatgpt.uc.edu/api/v1/")
    LLM_ACCESS_TOKEN: str = os.getenv("LLM_ACCESS_TOKEN", "sk-ce534a4abbe64dd3a51bb50d9985d6f1")

settings = AppSettings()