from src.dao import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, JSON
import uuid
from player import Player


class Match(Base):
    __tablename__ = "matches"

    uuid: Mapped[uuid.UUID]
    player1: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    player2: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    winner: Mapped[int] = mapped_column(Integer, ForeignKey("players.id"))
    score: Mapped[str] = mapped_column(JSON)

    players: Mapped[list["Player"]] = relationship("Player", back_populates="matches")