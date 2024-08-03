from abc import ABC, abstractmethod
from typing import Any, Iterable


class IDataClient(ABC):
    @abstractmethod
    async def get_data(self) -> Iterable[dict[str, Any]]:
        ...


class MemoryDataClient(IDataClient):
    def __init__(self):
        self._data = []

    async def get_data(self) -> Iterable[dict[str, Any]]:
        return self._data
