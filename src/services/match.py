from src.schemas import CreateMatchRequest, Match, MatchesFilters, GetMatchesRequest, Score
from src.services import PlayerService
from src.dao import MatchDAO
from src.match_manager.match_observer import MatchObserver
from math import ceil
import logging
from src.utils.exceptions import DatabaseNotFoundError

logger = logging.getLogger(__name__)


class MatchService:
    matches_at_page: int = 5

    @staticmethod
    def add_match_service(match_data: CreateMatchRequest) -> Match:
        player1 = PlayerService.get_or_add_player(name=match_data.player1_name)
        player2 = PlayerService.get_or_add_player(name=match_data.player2_name)

        match_data = Match(player1=player1,
                           player2=player2,
                           score=Score(is_best_of_five=match_data.is_best_of_five))

        match = MatchDAO.add_match(match_data=match_data)

        return Match.from_orm(match)

    @staticmethod
    def get_match_service(match_uuid: str):
        match = MatchDAO.get_match_by_uuid(match_uuid=match_uuid)
        if match is None:
            raise DatabaseNotFoundError(message="Match not found")
        return Match.from_orm(match)

    @classmethod
    def update_match_service(cls, match_uuid: str, player_win: int) -> Match:
        match: Match = cls.get_match_service(match_uuid=match_uuid)
        match_observer = MatchObserver(match_data=match.score)
        match_observer.add_points(player_idx=player_win)

        if match_observer.check_winner_exists():
            match.winner = match.player1 if player_win == 0 else match.player2
        match.score = match_observer.get_data()
        MatchDAO.update_match(match_uuid=match_uuid, match_data=match)
        return match

    @classmethod
    def get_matches_service(cls, match_filters: GetMatchesRequest) -> list[Match]:
        offset = (match_filters.page_number - 1) * cls.matches_at_page
        filters = MatchesFilters(limit=cls.matches_at_page,
                                 offset=offset,
                                 player_name=match_filters.filter_by_player_name,
                                 finished=match_filters.finished,
                                 ongoing=match_filters.ongoing)

        matches_orm = MatchDAO.get_matches(filters=filters)
        matches = [Match.from_orm(match) for match in matches_orm]
        return matches

    @classmethod
    def get_matches_pages_service(cls, match_filters: GetMatchesRequest) -> int:
        filters = MatchesFilters(player_name=match_filters.filter_by_player_name,
                                 finished=match_filters.finished,
                                 ongoing=match_filters.ongoing)

        count = MatchDAO.get_matches_count(filters)
        return ceil(count / cls.matches_at_page)
