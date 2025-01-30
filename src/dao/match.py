from src.schemas import Match, MatchesFilters
from src.models import MatchORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.sql import func, Select
from .database import connection
import logging
from src.utils.exceptions import DatabaseInternalError

logger = logging.getLogger(__name__)


class MatchDAO:
    @staticmethod
    @connection
    async def add_match(match_data: Match, session: AsyncSession) -> MatchORM:
        match = MatchORM(player1_id=match_data.player1.id,
                         player2_id=match_data.player2.id,
                         score=match_data.score.model_dump())
        session.add(match)
        try:
            await session.commit()
            await session.refresh(match)
            return match
        except Exception as e:
            logger.error(e)
            raise DatabaseInternalError

    @staticmethod
    @connection
    async def get_match_by_uuid(match_uuid: str, session: AsyncSession) -> MatchORM:
        query = select(MatchORM).filter_by(uuid=match_uuid)
        try:
            result = await session.execute(query)
            match = result.scalars().first()
            return match
        except Exception as e:
            logger.error(e)
            raise DatabaseInternalError

    @classmethod
    @connection
    async def get_matches(cls, filters: MatchesFilters,
                          session: AsyncSession) -> list[MatchORM]:

        query = select(MatchORM).limit(limit=filters.limit).offset(offset=filters.offset).order_by(MatchORM.id.desc())
        query = await cls._apply_match_filters(query=query, filters=filters)

        try:
            result = await session.execute(query)
            matches = list(result.scalars().all())
            return matches
        except Exception as e:
            logger.error(e)
            raise DatabaseInternalError

    @classmethod
    @connection
    async def get_matches_count(cls, filters: MatchesFilters, session: AsyncSession) -> int:
        query = select(func.count()).select_from(MatchORM)
        query = await cls._apply_match_filters(query=query, filters=filters)

        try:
            result = await session.execute(query)
            count = result.scalar()
            return count
        except Exception as e:
            logger.error(e)
            raise DatabaseInternalError

    @staticmethod
    @connection
    async def update_match(match_uuid: str, match_data: Match, session: AsyncSession):
        query = update(MatchORM).where(MatchORM.uuid == match_uuid).values(score=match_data.score.model_dump(),
                                                                           winner_id=match_data.winner.id if match_data.winner else None)

        try:
            await session.execute(query)
            await session.commit()
        except Exception as e:
            logger.error(e)
            raise DatabaseInternalError

    @staticmethod
    async def _apply_match_filters(query: Select, filters: MatchesFilters):
        if filters.player_name:
            query = query.where(
                (MatchORM.player1.has(name=filters.player_name)) | (MatchORM.player2.has(name=filters.player_name)))
        if filters.finished != filters.ongoing:
            if filters.finished:
                query = query.where(MatchORM.winner_id.isnot(None))
            else:
                query = query.where(MatchORM.winner_id.is_(None))

        return query
