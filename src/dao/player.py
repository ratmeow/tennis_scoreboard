from .database import connection
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models import PlayerORM
from typing import Optional

import logging
from src.utils.exceptions import DatabaseInternalError

logger = logging.getLogger(__name__)


class PlayerDAO:
    @classmethod
    @connection
    async def get_player_or_none(cls, name: str, session: AsyncSession) -> Optional[PlayerORM]:
        query = select(PlayerORM).filter_by(name=name)
        try:
            result = await session.execute(query)
            player_info = result.scalar_one_or_none()
            return player_info
        except Exception as e:
            logger.error(e)
            raise DatabaseInternalError

    @classmethod
    @connection
    async def add_player(cls, name: str, session: AsyncSession):
        player = PlayerORM(name=name)
        session.add(player)
        try:
            await session.commit()
            return player
        except Exception as e:
            logger.error(e)
            raise DatabaseInternalError
