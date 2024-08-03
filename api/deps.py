from punq import Container, Scope

from api.data.client import MemoryDataClient, IDataClient
from api.data.handler import DataHandler
from api.data.router import DataRouter
from api.server import Server


class DepsContainer(Container):
    def __init__(self):
        super().__init__()
        self.register(IDataClient, MemoryDataClient, scope=Scope.singleton)
        self.register(DataHandler, DataHandler, scope=Scope.singleton)
        self.register(DataRouter, DataRouter, scope=Scope.singleton)
        self.register(Server, Server, scope=Scope.singleton)
