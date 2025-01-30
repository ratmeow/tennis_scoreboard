from src.dao import PlayerDAO
from typing import Optional
from src.schemas import Player


class PlayerService:
    @staticmethod
    async def add_player_service(name: str) -> Player:
        player_db = await PlayerDAO.add_player(name=name)
        return Player.from_orm(player_db)

    @staticmethod
    async def get_player_service(name: str) -> Optional[Player]:
        player_db = await PlayerDAO.get_player_or_none(name=name)
        return Player.from_orm(player_db) if player_db else None

    @classmethod
    async def get_or_add_player(cls, name: str) -> Player:
        player = await PlayerService.get_player_service(name=name)
        if player is None:
            player = await PlayerService.add_player_service(name=name)
        return player
