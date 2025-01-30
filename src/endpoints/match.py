from typing import Annotated
from fastapi import APIRouter, Form, Query, Request, HTTPException
from fastapi.responses import RedirectResponse
from src.schemas import CreateMatchRequest, GetMatchesRequest, GetMatchesResponse
from src.services import MatchService
from src import templates
from src.utils.exceptions import DatabaseInternalError, ServiceValidationError, DatabaseNotFoundError
from src.utils.validator import FieldValidator

router = APIRouter(tags=["match"])


@router.post("/new-match")
async def add_match_api(request: Request, match_data: Annotated[CreateMatchRequest, Form()]):
    try:
        FieldValidator.validate_player_names(player1_name=match_data.player1_name,
                                             player2_name=match_data.player2_name)

        match = await MatchService.add_match_service(match_data=match_data)

        return RedirectResponse(url=f"/match-score/?uuid={match.uuid}", status_code=303)

    except ServiceValidationError as e:
        return templates.TemplateResponse(name="new-match.html", context={"request": request, "error": e.message})
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.get("/new-match")
async def get_new_match_api(request: Request):
    return templates.TemplateResponse(name="new-match.html", context={"request": request})


@router.get("/match-score/")
async def get_match_api(request: Request, uuid: str):
    try:
        match = await MatchService.get_match_service(match_uuid=uuid)
        if match.winner:
            return RedirectResponse(url=f"/match-result/?uuid={uuid}")
        return templates.TemplateResponse(name="match-score.html", context={"request": request, "match": match.dict()})
    except DatabaseNotFoundError as e:
        return templates.TemplateResponse(name="index.html", context={"request": request, "error": e.message})
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.post("/match-score/")
async def update_match_api(request: Request, uuid: str, player_win: Annotated[int, Form()]):
    try:
        redirect_url = "match-score"
        match = await MatchService.update_match_service(match_uuid=uuid, player_win=player_win)
        if match.winner:
            redirect_url = "match-result"
        return RedirectResponse(url=f"/{redirect_url}/?uuid={uuid}", status_code=303)

    except DatabaseNotFoundError as e:
        return templates.TemplateResponse(name="index.html", context={"request": request, "error": e.message})
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.get("/match-result/")
async def get_match_result_api(request: Request, uuid: str):
    try:
        match = await MatchService.get_match_service(match_uuid=uuid)
        return templates.TemplateResponse(name="match-result.html", context={"request": request, "match": match.dict()})
    except DatabaseNotFoundError as e:
        return templates.TemplateResponse(name="index.html", context={"request": request, "error": e.message})
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)


@router.get("/matches/")
async def get_matches_api(request: Request, match_filters: Annotated[GetMatchesRequest, Query()]):
    try:
        if match_filters.filter_by_player_name:
            FieldValidator.validate_name(name=match_filters.filter_by_player_name,
                                         field="Player name")

        matches = await MatchService.get_matches_service(match_filters=match_filters)
        total_pages = await MatchService.get_matches_pages_service(match_filters=match_filters)
        response = GetMatchesResponse(matches=matches,
                                      total_pages=total_pages,
                                      match_filters=match_filters)
    except ServiceValidationError as e:
        response = GetMatchesResponse(match_filters=match_filters,
                                      error=e.message)
    except DatabaseInternalError as e:
        raise HTTPException(status_code=500, detail=e.message)

    return templates.TemplateResponse(name="matches.html",
                                      context={"request": request, **response.model_dump()})
