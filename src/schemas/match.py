from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .player import Player


class CreateMatchRequest(BaseModel):
    player1_name: str = Field(alias="playerOne")
    player2_name: str = Field(alias="playerTwo")
    is_best_of_five: bool = False

    @field_validator("player1_name", "player2_name")
    def validate_player_name(cls, value):
        return value.lower()


class GetMatchesRequest(BaseModel):
    page_number: int = 1
    filter_by_player_name: str = Field(default="")
    finished: bool = False
    ongoing: bool = False


class MatchesFilters(BaseModel):
    limit: int = -1
    offset: int = 0
    player_name: Optional[str] = None
    finished: bool
    ongoing: bool


class Score(BaseModel):
    points: list[int] = [0, 0]
    games: list[list[int]] = [[0, 0]]
    sets: list[int] = [0, 0]
    is_best_of_five: bool


class Match(BaseModel):
    uuid: str = None
    player1: Player
    player2: Player
    winner: Optional[Player] = None
    score: Score

    model_config = ConfigDict(from_attributes=True)


class GetMatchesResponse(BaseModel):
    matches: list[Match] = []
    total_pages: int = 0
    match_filters: GetMatchesRequest
    error: Optional[str] = None
