from fastapi import FastAPI

from api.data.router import DataRouter


class Server(FastAPI):
    def __init__(
        self, data_router: DataRouter
    ):
        super().__init__()
        self.include_router(data_router)
