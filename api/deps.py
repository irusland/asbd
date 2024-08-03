from punq import Container, Scope

from api.data.router import DataRouter, DataClient
from api.server import Server


class DepsContainer(Container):
    def __init__(self):
        super().__init__()
        self.register(DataClient, DataClient, scope=Scope.singleton)
        self.register(DataRouter, DataRouter, scope=Scope.singleton)
        self.register(Server, Server, scope=Scope.singleton)
