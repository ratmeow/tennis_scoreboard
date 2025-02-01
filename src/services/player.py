from typing import Optional

from src.dao.player import PlayerDAO
from src.schemas.player import Player


class PlayerService:
    @staticmethod
    def add_player_service(name: str) -> Player:
        player_db = PlayerDAO.add_player(name=name)
        return Player.from_orm(player_db)

    @staticmethod
    def get_player_service(name: str) -> Optional[Player]:
        player_db = PlayerDAO.get_player_or_none(name=name)
        return Player.from_orm(player_db) if player_db else None

    @classmethod
    def get_or_add_player(cls, name: str) -> Player:
        player = PlayerService.get_player_service(name=name)
        if player is None:
            player = PlayerService.add_player_service(name=name)
        return player
