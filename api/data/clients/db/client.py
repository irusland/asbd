from api.data.clients.db.base import BaseDBDataClient
from api.data.clients.db.settings import (
    DB1DataClientSettings,
    DB2DataClientSettings,
    DB3DataClientSettings
)
from api.data.db.models.user import User1, User2, User3


class DB1DataClient(BaseDBDataClient):
    """First data source client"""

    def __init__(self, settings: DB1DataClientSettings):
        super().__init__(settings, data_model=User1)


class DB2DataClient(BaseDBDataClient):
    """Second data source client"""

    def __init__(self, settings: DB2DataClientSettings):
        super().__init__(settings, data_model=User2)


class DB3DataClient(BaseDBDataClient):
    """Third data source client"""

    def __init__(self, settings: DB3DataClientSettings):
        super().__init__(settings, data_model=User3)
