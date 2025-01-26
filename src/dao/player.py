from .database import connection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import PlayerORM
from typing import Optional
import sqlite3
from src.utils import UniqueError


class PlayerDAO:
    @classmethod
    @connection
    async def get_player(cls, name: str, session: AsyncSession) -> Optional[PlayerORM]:
        query = select(PlayerORM).filter_by(name=name)
        result = await session.execute(query)
        player_info = result.scalar_one_or_none()
        return player_info

    @classmethod
    @connection
    async def add_player(cls, name: str, session: AsyncSession):
        try:
            player = PlayerORM(name=name)
            session.add(player)
            await session.commit()
            return player
        except sqlite3.IntegrityError as e:
            raise UniqueError(message="Player with this name already exists")
