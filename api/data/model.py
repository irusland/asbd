from typing import NewType

from pydantic import BaseModel

Name = NewType("Name", str)
Identifier = NewType("ID", int)


class Data(BaseModel):
    name: Name
    id: Identifier
