"""Configuration initialization.

See Pydantic docs for details.
These variables specify the defaults and structure.
Configuration is overriden by the corresponding value in the .env file or environment variable.

>>> import os
>>> os.environ.get("SQL_ALCHEMY_STRING")

is equivalent to

>>> conf.sql_alchemy_string
"""
from pydantic import BaseSettings, SecretStr


class Settings(BaseSettings):
    log_level: str = "WARNING"
    sql_alchemy_string: SecretStr
    read_buffer: int = 64

    class Config:
        env_file = ".env"


conf = Settings()
