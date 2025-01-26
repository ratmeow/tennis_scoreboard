from src.dao import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class PlayerORM(Base):
    __tablename__ = "players"
    name: Mapped[str] = mapped_column(nullable=False, index=True, unique=True)
    matches: Mapped[list["MatchORM"]] = relationship(primaryjoin="or_(MatchORM.player1_id == PlayerORM.id, "
                                                                 "MatchORM.player2_id == PlayerORM.id)",
                                                  viewonly=True)
