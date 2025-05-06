from pydantic import BaseSettings

class Settings(BaseSettings):
    pinecone_api_key: str
    pinecone_environment: str = "us-west1-gcp"
    redis_url: str = "redis://redis:6379/0"

    class Config:
        env_file = ".env"

settings = Settings()