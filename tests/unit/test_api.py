import pytest
from punq import Scope
from starlette.testclient import TestClient

from api.data.clients.interface import IDataClient
from api.data.clients.memory import MemoryDataClient
from api.deps import DepsContainer
from api.server import Server

@pytest.fixture()
def override_memory_data_client(deps_container: DepsContainer) -> None:
    deps_container.registrations[IDataClient].clear()
    deps_container.register(IDataClient, MemoryDataClient, scope=Scope.singleton)


@pytest.fixture()
def server(override_memory_data_client, deps_container: DepsContainer) -> Server:
    return deps_container.resolve(Server)


@pytest.fixture()
def client(server: Server) -> TestClient:
    return TestClient(server)


class TestServer:
    def test_gets_data(self, client: TestClient):
        response = client.get("/data")
        assert response.status_code == 200
        assert response.json() == []
