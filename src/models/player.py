from src.dao import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class PlayerORM(Base):
    __tablename__ = "players"
    name: Mapped[str] = mapped_column(nullable=False, index=True, unique=True)
