from src.dao import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from match import Match


class Player(Base):
    __tablename__ = "players"
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)

    matches: Mapped[list["Match"]] = relationship("Match", back_populates="players")