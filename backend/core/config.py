import os
import logging
from pydantic_settings import BaseSettings


logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    PROJECT_NAME: str = "TPV Verifactu"
    
    # Database configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://tpv:tpv_default_pwd@db:5432/tpv"  # Docker default
    )
    
    # Security
    MASTER_KEY_REPO: str = os.getenv("MASTER_KEY_REPO", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    # Dongle requirement (can be disabled for testing)
    DONGLE_REQUIRED: bool = True
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Application mode
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Check for test mode marker file
        if os.path.exists("test_mode.marker"):
            self.DONGLE_REQUIRED = False
            logger.warning("TEST MODE ACTIVE: Dongle check disabled")
        
        # Check environment variable override
        if os.getenv("DONGLE_REQUIRED", "").lower() == "false":
            self.DONGLE_REQUIRED = False
            logger.info("Dongle requirement disabled via environment variable")
        
        # Log database configuration (without password)
        db_url = self.DATABASE_URL
        if "@" in db_url:
            db_url = db_url.split("@")[1]  # Hide credentials in logs
        logger.info(f"Database URL: postgresql://{db_url}")
        
        # Validate database URL format
        if not self.DATABASE_URL.startswith("postgresql://"):
            logger.error("Invalid DATABASE_URL format. Must start with 'postgresql://'")
            raise ValueError("Invalid DATABASE_URL format")
    
    class Config:
        case_sensitive = True
        env_file = ".env"  # Support .env file
        env_file_encoding = "utf-8"


# Create global settings instance
settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

