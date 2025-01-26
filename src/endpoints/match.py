from typing import Annotated
from fastapi import APIRouter, Form, Path, Query, Request
from fastapi.responses import RedirectResponse
from src.schemas import CreateMatchRequest, GetMatchesRequest
from src.services import MatchService
from src.utils import WinnerAlreadyExists
from src import templates

router = APIRouter(tags=["match"])


@router.post("/new-match")
async def add_match_api(match_data: Annotated[CreateMatchRequest, Form()]):
    match = await MatchService.add_match_service(match_data=match_data)
    return RedirectResponse(url=f"/match-score/?uuid={match.uuid}", status_code=303)


@router.get("/new-match")
async def get_new_match_api(request: Request):
    return templates.TemplateResponse(name="new-match.html", context={"request": request})


@router.get("/match-score/")
async def get_match_api(request: Request, uuid: str):
    match = await MatchService.get_match_service(match_uuid=uuid)
    if match.winner:
        return RedirectResponse(url=f"/match-result/?uuid={uuid}")
    return templates.TemplateResponse(name="match-score.html", context={"request": request, "match": match.dict()})


@router.get("/match-result/")
async def get_match_result(request: Request, uuid: str):
    match = await MatchService.get_match_service(match_uuid=uuid)
    print(match)
    return templates.TemplateResponse(name="match-result.html", context={"request": request, "match": match.dict()})


@router.post("/match-score/")
async def update_match_api(uuid: str, player_win: Annotated[int, Form()]):
    redirect_url = "match-score"
    match = await MatchService.update_match_service(match_uuid=uuid, player_win=player_win)
    if match.winner:
        redirect_url = "match-result"
    return RedirectResponse(url=f"/{redirect_url}/?uuid={uuid}", status_code=303)


@router.get("/matches")
async def get_player_matches_api(request: Annotated[GetMatchesRequest, Query()]):
    pass
