from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # O Pydantic vai buscar essas chaves no seu .env
    OPENAI_API_KEY: str
    DATABASE_URL: str = "sqlite:///./test.db" # Valor padrão
    DEBUG: bool = False

    model_config = SettingsConfigDict(env_file=".env")

# Instância única para todo o projeto
settings = Settings()