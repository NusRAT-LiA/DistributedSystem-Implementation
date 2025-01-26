import os
from dotenv import load_dotenv


load_dotenv()


class Settings:

    pgHost: str = os.getenv("POSTGRES_HOST")
    pgPort: str = os.getenv("POSTGRES_PORT")
    pgDatabase: str = os.getenv("POSTGRES_DB")
    pgUsername: str = os.getenv("POSTGRES_USER")
    pgPassword: str = os.getenv("POSTGRES_PASSWORD")

settings = Settings()
