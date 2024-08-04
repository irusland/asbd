from api.data.clients.db.base import BaseDBDataClient
from api.data.clients.db.settings import (
    DB1DataClientSettings,
    DB2DataClientSettings,
    DB3DataClientSettings,
)


class DB1DataClient(BaseDBDataClient):
    """First data source client"""

    def __init__(self, settings: DB1DataClientSettings):
        super().__init__(settings)


class DB2DataClient(BaseDBDataClient):
    """Second data source client"""

    def __init__(self, settings: DB2DataClientSettings):
        super().__init__(settings)


class DB3DataClient(BaseDBDataClient):
    """Third data source client"""

    def __init__(self, settings: DB3DataClientSettings):
        super().__init__(settings)
