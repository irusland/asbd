import asyncio

import pytest
from jinja2 import Template

from api.data.clients.db.base import BaseDBDataClient
from api.data.clients.db.settings import DB1DataClientSettings
from api.data.db.models.user import User1
from api.data.model import Data
from db.fill_data import (
    CREATE_USERS_SQL_JINJA,
    Source,
    execute_sqls,
    render_create_sqls
)


class DBDataClient(BaseDBDataClient):
    def __init__(self, settings: DB1DataClientSettings):
        super().__init__(settings=settings, data_model=User1)


@pytest.fixture()
def data_ranges() -> list[tuple[int, int]]:
    return []


@pytest.fixture(autouse=True)
def fill_database(data_ranges: list[tuple[int, int]]):
    with open(CREATE_USERS_SQL_JINJA, 'r') as f:
        template = Template(f.read())
    sources = [
        Source(source_number=1, ranges=data_ranges),
    ]
    rendered_sqls = render_create_sqls(sources, template)
    asyncio.run(execute_sqls(rendered_sqls, [DB1DataClientSettings()], prompt=False))


@pytest.fixture()
def db_client_settings() -> DB1DataClientSettings:
    return DB1DataClientSettings(url='postgresql+asyncpg://irusland:password@0.0.0.0:5432/db')


@pytest.fixture()
def db_client(db_client_settings: DB1DataClientSettings) -> DBDataClient:
    return DBDataClient(settings=db_client_settings)


class TestBaseDBDataClient:
    @pytest.mark.asyncio
    @pytest.mark.parametrize('data_ranges', [[(1, 10), (31, 40)]])
    async def test_example_postgres(self, db_client: DBDataClient, data_ranges: list[tuple[int, int]]):
        expected = [Data(id=i, name=f'Test {i}') for a, b in data_ranges for i in range(a, b + 1)]

        result = await db_client.get_data()

        assert result == expected
