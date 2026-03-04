import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "TPV Verifactu"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://tpv:tpvpassword@localhost:5432/tpv")
    MASTER_KEY_REPO: str = os.getenv("MASTER_KEY_REPO", "")
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    DONGLE_REQUIRED: bool = True

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if os.path.exists("test_mode.marker"):
            self.DONGLE_REQUIRED = False
        elif os.getenv("DONGLE_REQUIRED", "True").lower() == "false":
             self.DONGLE_REQUIRED = False

    class Config:
        case_sensitive = True

settings = Settings()
