from abc import ABC, abstractmethod
from typing import Sequence

from api.data.model import Data


class IDataClient(ABC):
    @abstractmethod
    async def get_data(self) -> Sequence[Data]: ...
