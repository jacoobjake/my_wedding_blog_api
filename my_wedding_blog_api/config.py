from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    testing: str = "Default"
    mongo_db_host: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
