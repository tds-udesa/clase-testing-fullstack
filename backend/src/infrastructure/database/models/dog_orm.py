from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.models.base import Base


class Dog(Base):
    __tablename__ = "dogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column()
    url: Mapped[str] = mapped_column()
