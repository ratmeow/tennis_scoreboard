import logging

from sqlalchemy import select, update
from sqlalchemy.orm import Session
from sqlalchemy.sql import Select, func

from src.models.match import MatchORM
from src.schemas.match import Match, MatchesFilters

from .database import connection

logger = logging.getLogger(__name__)


class MatchDAO:
    @staticmethod
    @connection(commit=True)
    def add_match(match_data: Match, session: Session) -> MatchORM:
        match = MatchORM(
            player1_id=match_data.player1.id,
            player2_id=match_data.player2.id,
            score=match_data.score.model_dump(),
        )

        session.add(match)
        session.flush()
        session.refresh(match)
        return match

    @staticmethod
    @connection()
    def get_match_by_uuid(match_uuid: str, session: Session) -> MatchORM:
        query = select(MatchORM).filter_by(uuid=match_uuid)
        result = session.execute(query)
        match = result.scalars().first()
        return match

    @classmethod
    @connection()
    def get_matches(cls, filters: MatchesFilters, session: Session) -> list[MatchORM]:
        query = (
            select(MatchORM)
            .limit(limit=filters.limit)
            .offset(offset=filters.offset)
            .order_by(MatchORM.id.desc())
        )
        query = cls._apply_match_filters(query=query, filters=filters)

        result = session.execute(query)
        matches = list(result.scalars().all())
        return matches

    @classmethod
    @connection()
    def get_matches_count(cls, filters: MatchesFilters, session: Session) -> int:
        query = select(func.count()).select_from(MatchORM)
        query = cls._apply_match_filters(query=query, filters=filters)

        result = session.execute(query)
        count = result.scalar()
        return count

    @staticmethod
    @connection(commit=True)
    def update_match(match_uuid: str, match_data: Match, session: Session):
        query = (
            update(MatchORM)
            .where(MatchORM.uuid == match_uuid)
            .values(
                score=match_data.score.model_dump(),
                winner_id=match_data.winner.id if match_data.winner else None,
            )
        )

        session.execute(query)

    @staticmethod
    def _apply_match_filters(query: Select, filters: MatchesFilters):
        if filters.player_name:
            query = query.where(
                (MatchORM.player1.has(name=filters.player_name))
                | (MatchORM.player2.has(name=filters.player_name))
            )
        if filters.finished != filters.ongoing:
            if filters.finished:
                query = query.where(MatchORM.winner_id.isnot(None))
            else:
                query = query.where(MatchORM.winner_id.is_(None))

        return query
