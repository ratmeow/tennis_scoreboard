from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from .player import Player


class CreateMatchRequest(BaseModel):
    player1_name: str = Field(alias="playerOne")
    player2_name: str = Field(alias="playerTwo")


class GetMatchesRequest(BaseModel):
    page: int = 1
    filter_by_player_name: str = ""


class Score(BaseModel):
    points: list[int] = [0, 0]
    games: list[list[int]] = [[0, 0]]
    sets: list[int] = [0, 0]


class Match(BaseModel):
    player1: Player
    player2: Player
    winner: Optional[Player] = None
    score: Score = Field(default=Score())

    model_config = ConfigDict(from_attributes=True)


class MatchResponse(BaseModel):
    uuid: str
    player1_name: str
    player2_name: str
    score: dict

    model_config = ConfigDict(from_attributes=True)
