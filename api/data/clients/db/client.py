from typing import Sequence

from api.data.clients.db.settings import (
    BaseDBDataClientSettings,
    DB1DataClientSettings,
    DB2DataClientSettings,
    DB3DataClientSettings,
)
from api.data.clients.interface import IDataClient
from api.data.model import Data


class BaseDBDataClient(IDataClient):
    def __init__(self, settings: BaseDBDataClientSettings):
        self._settings = settings

    async def get_data(self) -> Sequence[Data]:
        return [Data(id=1, name=self._settings.__repr_name__())]


class DB1DataClient(BaseDBDataClient):
    def __init__(self, settings: DB1DataClientSettings):
        super().__init__(settings)


class DB2DataClient(BaseDBDataClient):
    def __init__(self, settings: DB2DataClientSettings):
        super().__init__(settings)


class DB3DataClient(BaseDBDataClient):
    def __init__(self, settings: DB3DataClientSettings):
        super().__init__(settings)
