from datetime import timedelta

from pydantic.v1 import BaseSettings


class BaseDBDataClientSettings(BaseSettings):
    host: str = "0.0.0.0"
    port: int = 5432
    user: str
    password: str
    database: str = "db"

    connect_timeout: timedelta = timedelta(seconds=1)
    read_timeout: timedelta = timedelta(seconds=2)


class DB1DataClientSettings(BaseDBDataClientSettings):
    class Config:
        env_prefix = "DB1_"


class DB2DataClientSettings(BaseDBDataClientSettings):
    class Config:
        env_prefix = "DB2_"


class DB3DataClientSettings(BaseDBDataClientSettings):
    class Config:
        env_prefix = "DB3_"
