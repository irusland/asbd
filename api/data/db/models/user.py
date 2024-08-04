from sqlalchemy.orm import Mapped, mapped_column

from api.data.db.models.base import Base
from api.data.model import Identifier, Name


class User(Base):
    __tablename__ = "user"

    id: Mapped[Identifier] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[Name]
