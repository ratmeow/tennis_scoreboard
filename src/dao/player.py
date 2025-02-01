from .database import connection
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.models import PlayerORM
from typing import Optional

import logging

logger = logging.getLogger(__name__)


class PlayerDAO:
    @classmethod
    @connection()
    def get_player_or_none(cls, name: str, session: Session) -> Optional[PlayerORM]:
        query = select(PlayerORM).filter_by(name=name)

        result = session.execute(query)
        player_info = result.scalar_one_or_none()
        return player_info

    @classmethod
    @connection(commit=True)
    def add_player(cls, name: str, session: Session):
        player = PlayerORM(name=name)
        session.add(player)
        return player
