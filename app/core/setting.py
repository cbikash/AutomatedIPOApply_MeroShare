import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME = os.getenv("PROJECT_NAME", "MyApp")
    PROJECT_VERSION = os.getenv("PROJECT_VERSION", "0.1.0")

    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "")
    API_VERSION = os.getenv("API_VERSION", "v1")
    ENCRYPTION_KEY= os.getenv("ENCRYPTION_KEY", '')

    MEROSHARE_URL = os.getenv("BASE_URL_MEROSHARE")

settings = Settings()