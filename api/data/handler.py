import operator
from asyncio import gather
from itertools import chain

from api.data.clients.interface import IDataClient
from api.data.model import Data


class DataHandler:
    def __init__(self, data_clients: list[IDataClient]):
        self._data_clients = data_clients

    async def read_data(self) -> list[Data]:
        data_parts = await gather(
            *[data_client.get_data() for data_client in self._data_clients]
        )
        return sorted(chain(*data_parts), key=operator.attrgetter("id"))
