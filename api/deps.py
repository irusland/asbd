from punq import Container, Scope
from pydantic.v1 import BaseSettings

from api.data.clients.db.client import DB1DataClient, DB2DataClient, DB3DataClient
from api.data.clients.db.settings import (
    DB1DataClientSettings,
    DB2DataClientSettings,
    DB3DataClientSettings,
)
from api.data.clients.interface import IDataClient
from api.data.handler import DataHandler
from api.data.router import DataRouter
from api.server import Server


class DepsContainer(Container):
    def __init__(self):
        super().__init__()
        self.register_settings(DB1DataClientSettings)
        self.register(IDataClient, DB1DataClient, scope=Scope.singleton)
        self.register_settings(DB2DataClientSettings)
        self.register(IDataClient, DB2DataClient, scope=Scope.singleton)
        self.register_settings(DB3DataClientSettings)
        self.register(IDataClient, DB3DataClient, scope=Scope.singleton)
        self.register(DataHandler, DataHandler, scope=Scope.singleton)
        self.register(DataRouter, DataRouter, scope=Scope.singleton)
        self.register(Server, Server, scope=Scope.singleton)

    def register_settings(self, settings: type[BaseSettings]) -> None:
        self.register(settings, lambda: settings(), scope=Scope.singleton)
