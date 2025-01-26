from src.schemas import Match, Score
from src.models import MatchORM
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from .database import connection


class MatchDAO:
    @staticmethod
    @connection
    async def add_match(match_data: Match, session: AsyncSession) -> MatchORM:
        match = MatchORM(player1_id=match_data.player1.id,
                         player2_id=match_data.player2.id,
                         score=match_data.score.model_dump())
        session.add(match)
        await session.commit()
        await session.refresh(match)
        return match

    @staticmethod
    @connection
    async def get_match_by_uuid(match_uuid: str, session: AsyncSession) -> MatchORM:
        query = select(MatchORM).filter_by(uuid=match_uuid)
        result = await session.execute(query)

        match = result.scalars().first()
        return match

    @staticmethod
    @connection
    async def get_matches_by_player(player_name: str, session: AsyncSession):
        pass

    @staticmethod
    @connection
    async def update_match(match_uuid: str, match_data: Match, session: AsyncSession):
        query = update(MatchORM).where(MatchORM.uuid == match_uuid).values(score=match_data.score.model_dump(),
                                                                           winner_id=match_data.winner.id if match_data.winner else None)

        await session.execute(query)
        await session.commit()
