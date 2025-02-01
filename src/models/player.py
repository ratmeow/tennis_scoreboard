from sqlalchemy.orm import Mapped, mapped_column

from src.dao.database import Base


class PlayerORM(Base):
    __tablename__ = "players"
    name: Mapped[str] = mapped_column(nullable=False, index=True, unique=True)
