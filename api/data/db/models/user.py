from sqlalchemy.orm import Mapped, mapped_column

from api.data.db.models.base import Base


class AbstractUser(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    name: Mapped[str]


class User1(AbstractUser):
    __tablename__ = 'data_1'


class User2(AbstractUser):
    __tablename__ = 'data_2'


class User3(AbstractUser):
    __tablename__ = 'data_3'
