from src.dao import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Integer, JSON
import uuid


class MatchORM(Base):
    __tablename__ = "matches"

    uuid: Mapped[str] = mapped_column(default=lambda: str(uuid.uuid4()))
    player1_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player2_id: Mapped[int] = mapped_column(ForeignKey("players.id"))
    winner_id: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=True)
    score: Mapped[dict] = mapped_column(JSON)

    player1: Mapped["PlayerORM"] = relationship(foreign_keys=[player1_id], uselist=False, lazy="joined")
    player2: Mapped["PlayerORM"] = relationship(foreign_keys=[player2_id], uselist=False, lazy="joined")
    winner: Mapped["PlayerORM"] = relationship(foreign_keys=[winner_id], uselist=False, lazy="joined")
