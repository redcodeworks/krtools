from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    log_level: str = "WARNING"
    sql_alchemy_string: SecretStr = "sqlite://"
    read_buffer: int = 64

    class Config:
        env_file = ".env"


conf = Settings()