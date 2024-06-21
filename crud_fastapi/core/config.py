from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_enconding="utf-8",
        env_ignore_empty=True
    )
    
    DATABASE_URL: str
    
    
settings = Settings()