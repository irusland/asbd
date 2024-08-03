import pytest

from api.deps import DepsContainer

@pytest.fixture()
def deps_container() -> DepsContainer:
    return DepsContainer()
