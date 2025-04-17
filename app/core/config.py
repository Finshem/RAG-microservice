from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    openai_api_url: str
    openai_api_key: str
    model: str
    temperature: float = 0.7
    max_tokens: int = 512

    class Config:
        env_file = ".env"

settings = Settings()
