from http import HTTPMethod
from textwrap import dedent

from fastapi import APIRouter

from api.data.model import Data


class DataClient:
    pass


class DataRouter(APIRouter):
    def __init__(self,
        data_client: DataClient
    ):
        super().__init__()
        self._data_client = data_client
        self.add_api_route(
            path="/data",
            endpoint=self._read_data,
            methods=[HTTPMethod.GET],
            response_model=list[Data],
            description=dedent("""\
                This endpoint retrieves records from three separate data sources in an asynchronous manner. 
                Each data source contains unique records identified by a sequential range of IDs. 
                After collecting the data, the endpoint combines results from all sources into a single list. 
                """
            )

        )

    async def _read_data(self):
        return []
        # try:
        #     return await self._data_client.get_all_data_sorted()
        # except Exception as e:
        #     raise HTTPException(status_code=500, detail=str(e))