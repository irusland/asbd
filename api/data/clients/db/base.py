from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from api.data.clients.db.settings import BaseDBDataClientSettings
from api.data.clients.interface import IDataClient
from api.data.db.models.user import User
from api.data.model import Data, Name


class BaseDBDataClient(IDataClient):
    def __init__(self, settings: BaseDBDataClientSettings):
        self._settings = settings
        engine = create_async_engine(
            settings.url,
            echo=settings.echo,
            connect_args={
                "connect_timeout": settings.connect_timeout.total_seconds(),
                "read_timeout": settings.read_timeout.total_seconds(),
            },
        )
        self._async_session = async_sessionmaker(engine, expire_on_commit=False)

    async def get_data(self) -> Sequence[Data]:
        async with self._async_session() as session:
            async with session.begin():
                session.add_all(
                    [
                        User(name=Name("test")),
                    ]
                )

            stmt = select(User)

            result = await session.scalars(stmt)

            [Data.model_validate(user) for user in result]
