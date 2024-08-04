from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from api.data.clients.db.settings import BaseDBDataClientSettings
from api.data.clients.interface import IDataClient
from api.data.db.models.user import AbstractUser
from api.data.model import Data


class BaseDBDataClient(IDataClient):
    def __init__(
        self, settings: BaseDBDataClientSettings, data_model: type[AbstractUser]
    ):
        self._settings = settings
        engine = create_async_engine(
            settings.url,
            echo=settings.echo,
            connect_args={
                "timeout": settings.timeout.total_seconds(),
            },
        )
        self._async_session = async_sessionmaker(engine, expire_on_commit=False)
        self._data_model = data_model

    async def get_data(self) -> Sequence[Data]:
        async with self._async_session() as session:
            statement = select(self._data_model)
            result = list(await session.scalars(statement))
            return [Data.model_validate(user.__dict__) for user in result]
