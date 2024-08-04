import pytest
from punq import Scope
from starlette.testclient import TestClient

from api.data.clients.interface import IDataClient
from api.data.clients.memory import MemoryDataClient
from api.deps import DepsContainer
from api.server import Server


@pytest.fixture()
def memory_data_client(mocker) -> MemoryDataClient:
    client = MemoryDataClient()
    client.get_data = mocker.AsyncMock(wraps=client.get_data)
    return client


@pytest.fixture()
def override_memory_data_client(deps_container: DepsContainer, memory_data_client: MemoryDataClient) -> None:
    deps_container.registrations[IDataClient].clear()
    deps_container.register(IDataClient, instance=memory_data_client, scope=Scope.singleton)


@pytest.fixture()
def server(override_memory_data_client, deps_container: DepsContainer) -> Server:
    return deps_container.resolve(Server)


@pytest.fixture()
def client(server: Server) -> TestClient:
    return TestClient(server)


def async_raise_func(exception: Exception):
    async def _async_raise_func():
        raise exception
    return _async_raise_func


class TestServer:
    def test_gets_data(self, client: TestClient):
        response = client.get("/data")
        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_ignores_data_when_error(self, client: TestClient, memory_data_client: MemoryDataClient):
        memory_data_client.get_data = async_raise_func(Exception('Error'))

        response = client.get("/data")

        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_ignores_data_when_timeout_error(self, client: TestClient, memory_data_client: MemoryDataClient):
        memory_data_client.get_data = async_raise_func(TimeoutError())

        response = client.get("/data")

        assert response.status_code == 200
        assert response.json() == []
