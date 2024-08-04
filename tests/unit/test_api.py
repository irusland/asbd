import random

import pytest
from punq import Scope
from starlette.testclient import TestClient

from api.data.clients.interface import IDataClient
from api.data.clients.memory import MemoryDataClient
from api.data.model import Data
from api.deps import DepsContainer
from api.server import Server


def _get_client_mock(mocker) -> MemoryDataClient:
    client = MemoryDataClient()
    client.get_data = mocker.AsyncMock(wraps=client.get_data)
    return client

@pytest.fixture()
def memory_data_client1(mocker) -> MemoryDataClient:
    return _get_client_mock(mocker)
@pytest.fixture()
def memory_data_client2(mocker) -> MemoryDataClient:
    return _get_client_mock(mocker)
@pytest.fixture()
def memory_data_client3(mocker) -> MemoryDataClient:
    return _get_client_mock(mocker)



@pytest.fixture()
def override_memory_data_client(deps_container: DepsContainer,
    memory_data_client1: MemoryDataClient,
    memory_data_client2: MemoryDataClient,
    memory_data_client3: MemoryDataClient,
) -> None:
    deps_container.registrations[IDataClient].clear()
    deps_container.register(IDataClient, instance=memory_data_client1, scope=Scope.singleton)
    deps_container.register(IDataClient, instance=memory_data_client2, scope=Scope.singleton)
    deps_container.register(IDataClient, instance=memory_data_client3, scope=Scope.singleton)


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
    async def test_ignores_data_when_error(self, client: TestClient, memory_data_client1: MemoryDataClient):
        memory_data_client1.get_data = async_raise_func(Exception('Error'))

        response = client.get("/data")

        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_ignores_data_when_error_multiple_sources(self, client: TestClient, memory_data_client1: MemoryDataClient, memory_data_client2: MemoryDataClient):
        expected_data = [Data(id=1, name='Test 1')]
        memory_data_client1.get_data = async_raise_func(Exception('Error'))
        memory_data_client2.get_data.return_value = expected_data

        response = client.get("/data")

        assert response.status_code == 200
        assert response.json() == [data.model_dump() for data in expected_data]

    @pytest.mark.asyncio
    async def test_ignores_data_when_timeout_error(self, client: TestClient, memory_data_client1: MemoryDataClient):
        memory_data_client1.get_data = async_raise_func(TimeoutError())

        response = client.get("/data")

        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.asyncio
    async def test_sorts_data(self, client: TestClient, memory_data_client1: MemoryDataClient):
        sorted_data = [Data(id=i, name=f'Test {i}') for i in range(42)]
        shuffled_data = sorted_data.copy()
        random.shuffle(shuffled_data)
        assert shuffled_data != sorted_data, 'Data is not shuffled'
        memory_data_client1.get_data.return_value = shuffled_data

        response = client.get("/data")

        assert response.status_code == 200
        assert response.json() == [data.model_dump() for data in sorted_data]

    @pytest.mark.asyncio
    async def test_sorts_data_from_multiple_sources(self, client: TestClient, memory_data_client1: MemoryDataClient, memory_data_client2: MemoryDataClient, memory_data_client3: MemoryDataClient):
        sorted_data = [Data(id=i, name=f'Test {i}') for i in range(42)]
        shuffled_data = sorted_data.copy()
        random.shuffle(shuffled_data)
        assert shuffled_data != sorted_data, 'Data is not shuffled'
        data_parts = [shuffled_data[i::3] for i in range(3)]
        for data_part, memory_data_client in zip(data_parts, (memory_data_client1, memory_data_client2, memory_data_client3)):
            memory_data_client.get_data.return_value = data_part

        response = client.get("/data")

        assert response.status_code == 200
        assert response.json() == [data.model_dump() for data in sorted_data]
