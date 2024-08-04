import operator
from asyncio import gather
from itertools import chain

from api.data.clients.interface import IDataClient
from api.data.model import Data


class DataHandler:
    def __init__(self, data_clients: list[IDataClient]):
        self._data_clients = data_clients

    async def read_data(self) -> list[Data]:
        coroutines = [data_client.get_data() for data_client in self._data_clients]

        data_parts_results = await gather(*coroutines, return_exceptions=True)
        data = chain.from_iterable(
            data_result for data_result in data_parts_results if
            not isinstance(data_result, BaseException)
        )
        return sorted(data, key=operator.attrgetter("id"))
