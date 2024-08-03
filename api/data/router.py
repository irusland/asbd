from http import HTTPMethod
from textwrap import dedent

from fastapi import APIRouter

from api.data.handler import DataHandler
from api.data.model import Data


class DataRouter(APIRouter):
    def __init__(self, data_handler: DataHandler):
        super().__init__()

        self.add_api_route(
            path="/data",
            endpoint=data_handler.read_data,
            methods=[HTTPMethod.GET],
            response_model=list[Data],
            description=dedent(
                """\
                This endpoint retrieves records from three separate data sources in an asynchronous manner. 
                Each data source contains unique records identified by a sequential range of IDs. 
                After collecting the data, the endpoint combines results from all sources into a single list. 
                """
            ),
        )
