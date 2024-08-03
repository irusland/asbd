import pytest
from starlette.testclient import TestClient

from api.deps import DepsContainer
from api.server import Server


@pytest.fixture()
def server(deps_container: DepsContainer) -> Server:
    return deps_container.resolve(Server)

@pytest.fixture()
def client(server: Server) -> TestClient:
    return TestClient(server)


class TestServer:
    def test_gets_data(self, client: TestClient):
        response = client.get("/data")
        assert response.status_code == 200
        assert response.json() == []
