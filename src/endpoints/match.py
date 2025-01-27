from typing import Annotated
from fastapi import APIRouter, Form, Path, Query, Request
from fastapi.responses import RedirectResponse
from src.schemas import CreateMatchRequest, GetMatchesRequest
from src.services import MatchService, PlayerService
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


@router.get("/matches/")
async def get_matches_api(request: Request, match_filters: Annotated[GetMatchesRequest, Query()]):
    print(match_filters)
    matches = await MatchService.get_matches_service(match_filters=match_filters)
    total_pages = await MatchService.get_matches_pages_service(match_filters=match_filters)
    print(match_filters.page_number)
    return templates.TemplateResponse(name="matches.html",
                                      context={"request": request,
                                               "matches": [match.dict() for match in matches],
                                               "page_number": match_filters.page_number,
                                               "total_pages": total_pages,
                                               "match_filters": match_filters})
