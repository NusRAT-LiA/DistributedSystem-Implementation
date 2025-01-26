import os
from dotenv import load_dotenv


load_dotenv()

class Settings:
    minioEndpoint: str = os.getenv("MINIO_ENDPOINT")
    minioAccessKey: str = os.getenv("MINIO_ACCESS_KEY")
    minioSecretKey: str = os.getenv("MINIO_SECRET_KEY")

    pgHost: str = os.getenv("POSTGRES_HOST")
    pgPort: str = os.getenv("POSTGRES_PORT")
    pgDatabase: str = os.getenv("POSTGRES_DB")
    pgUsername: str = os.getenv("POSTGRES_USER")
    pgPassword: str = os.getenv("POSTGRES_PASSWORD")

    

settings = Settings()
