from typing import Sequence

from api.data.clients.interface import IDataClient
from api.data.model import Data


class MemoryDataClient(IDataClient):
    def __init__(self):
        self._data = []

    async def get_data(self) -> Sequence[Data]:
        return self._data
