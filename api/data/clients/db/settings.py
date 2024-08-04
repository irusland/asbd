from datetime import timedelta

from pydantic import AnyUrl
from pydantic.v1 import BaseSettings


class BaseDBDataClientSettings(BaseSettings):
    url: str

    echo: bool = True

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
