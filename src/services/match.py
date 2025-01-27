from src.schemas import CreateMatchRequest, Match, MatchResponse, MatchesFilters, GetMatchesRequest
from src.services import PlayerService
from src.dao import MatchDAO
from src.match_manager.match_observer import MatchObserver
from math import ceil


class MatchService:
    matches_at_page: int = 5

    @staticmethod
    async def add_match_service(match_data: CreateMatchRequest) -> MatchResponse:
        player1 = await PlayerService.get_or_add_player(name=match_data.player1_name)
        player2 = await PlayerService.get_or_add_player(name=match_data.player2_name)

        match_data = Match(player1=player1,
                           player2=player2)

        match = await MatchDAO.add_match(match_data=match_data)

        match_response = MatchResponse(uuid=match.uuid,
                                       player1_name=player1.name,
                                       player2_name=player2.name,
                                       score=match.score)

        return match_response

    @staticmethod
    async def get_match_service(match_uuid: str):
        match = await MatchDAO.get_match_by_uuid(match_uuid=match_uuid)
        return Match.from_orm(match)

    @classmethod
    async def update_match_service(cls, match_uuid: str, player_win: int) -> Match:
        match: Match = await cls.get_match_service(match_uuid=match_uuid)
        match_observer = MatchObserver(match_data=match.score)
        match_observer.add_points(player_idx=player_win)
        if match_observer.check_winner_exists():
            match.winner = match.player1 if player_win == 0 else match.player2
        match.score = match_observer.get_data()
        await MatchDAO.update_match(match_uuid=match_uuid, match_data=match)
        return match

    @classmethod
    async def get_matches_service(cls, match_filters: GetMatchesRequest) -> list[Match]:
        player_name = match_filters.filter_by_player_name if len(match_filters.filter_by_player_name) > 0 else None
        offset = (match_filters.page_number - 1) * cls.matches_at_page
        filters = MatchesFilters(limit=cls.matches_at_page,
                                 offset=offset,
                                 player_name=player_name,
                                 finished=match_filters.finished,
                                 ongoing=match_filters.ongoing)

        matches_orm = await MatchDAO.get_matches(filters=filters)

        matches = [Match.from_orm(match) for match in matches_orm]
        return matches

    @classmethod
    async def get_matches_pages_service(cls, match_filters: GetMatchesRequest) -> int:
        filters = MatchesFilters(player_name=match_filters.filter_by_player_name,
                                 finished=match_filters.finished,
                                 ongoing=match_filters.ongoing)
        count = await MatchDAO.get_matches_count(filters)
        return ceil(count / cls.matches_at_page)
