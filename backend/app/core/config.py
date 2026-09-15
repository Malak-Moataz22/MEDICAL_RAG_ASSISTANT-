from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "RAG Assistant API"
    VECTOR_STORE_PATH: str = "backend/data/vector_store"
    OLLAMA_MODEL: str = "llama3.2:3b"

    class Config:
        env_file = ".env"

settings = Settings()