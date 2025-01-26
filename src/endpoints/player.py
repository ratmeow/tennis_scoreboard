from typing import Annotated
from fastapi import APIRouter, Form
from src.services import PlayerService
from src.schemas import Player

router = APIRouter(tags=["player"])


@router.post("/player")
async def add_player_api(name: Annotated[str, Form()]) -> Player:
    player = await PlayerService.add_player_service(name=name)
    return player


@router.get("/player")
async def get_player_api(name: str) -> Player:
    player = await PlayerService.get_player_service(name=name)
    return player
