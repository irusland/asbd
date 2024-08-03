from typing import Any

from api.data.client import IDataClient


class DataHandler:
    def __init__(self, data_client: IDataClient):
        self._data_client = data_client

    async def read_data(self) -> list[dict[str, Any]]:
        return sorted(await self._data_client.get_data(), key=lambda x: x["id"])
