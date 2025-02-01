from src.schemas.match import CreateMatchRequest, GetMatchesRequest, GetMatchesResponse
from src.server.renderer import Renderer
from src.server.router import Router
from src.services.match import MatchService
from src.utils.exceptions import (
    DatabaseInternalError,
    DatabaseNotFoundError,
    ServiceValidationError,
)
from src.utils.parser import Parser
from src.utils.validator import FieldValidator

router = Router()
renderer = Renderer(templates_dir="src/frontend")


def database_error_handler(method):
    def wrapper(environ, start_response, *args, **kwargs):
        try:
            return method(environ, start_response, *args, **kwargs)
        except (DatabaseNotFoundError, DatabaseInternalError) as e:
            status = "500"
            if isinstance(e, DatabaseNotFoundError):
                status = "404"
            return renderer.render_template(
                template_name="index.html",
                context={"error": e.message},
                start_response=start_response,
                status=status,
            )

    return wrapper


@router.get("/")
def get_root(environ, start_response):
    return renderer.render_template(template_name="index.html", start_response=start_response)


@router.get("/new-match")
def get_new_match_api(environ, start_response):
    return renderer.render_template(template_name="new-match.html", start_response=start_response)


@router.post("/new-match")
@database_error_handler
def add_match_api(environ, start_response):
    raw_data = Parser.parse_form_data(environ=environ)
    match_data = CreateMatchRequest(**raw_data)
    try:
        FieldValidator.validate_player_names(
            player1_name=match_data.player1_name, player2_name=match_data.player2_name
        )

        match = MatchService.add_match_service(match_data=match_data)

        start_response("303 See Other", [("Location", f"/match-score/?uuid={match.uuid}")])
        return []

    except ServiceValidationError as e:
        return renderer.render_template(
            template_name="new-match.html",
            context={"error": e.message},
            start_response=start_response,
        )


@router.get("/match-score/")
@database_error_handler
def get_match_api(environ, start_response):
    data = Parser.parse_query_data(environ=environ)
    match = MatchService.get_match_service(match_uuid=data["uuid"])
    if match.winner:
        start_response("303 See Other", [("Location", f"/match-result/?uuid={match.uuid}")])
        return []

    context = {"match": match.model_dump()}
    return renderer.render_template(
        template_name="match-score.html", context=context, start_response=start_response
    )


@router.post("/match-score/")
@database_error_handler
def update_match_api(environ, start_response):
    uuid = Parser.parse_query_data(environ=environ)["uuid"]
    player_win = int(Parser.parse_form_data(environ=environ)["player_win"])

    redirect_url = "match-score"
    match = MatchService.update_match_service(match_uuid=uuid, player_win=player_win)
    if match.winner:
        redirect_url = "match-result"

    start_response("303 See Other", [("Location", f"/{redirect_url}/?uuid={uuid}")])
    return []


@router.get("/match-result/")
@database_error_handler
def get_match_result_api(environ, start_response):
    uuid = Parser.parse_query_data(environ=environ)["uuid"]
    match = MatchService.get_match_service(match_uuid=uuid)
    return renderer.render_template(
        template_name="match-result.html",
        context={"match": match.dict()},
        start_response=start_response,
    )


@router.get("/matches/")
@database_error_handler
def get_matches_api(environ, start_response):
    raw_data = Parser.parse_query_data(environ=environ)
    match_filters = GetMatchesRequest(**raw_data)
    try:
        if match_filters.filter_by_player_name:
            FieldValidator.validate_name(
                name=match_filters.filter_by_player_name, field="Player name"
            )

        matches = MatchService.get_matches_service(match_filters=match_filters)
        total_pages = MatchService.get_matches_pages_service(match_filters=match_filters)
        context = GetMatchesResponse(
            matches=matches, total_pages=total_pages, match_filters=match_filters
        )
    except ServiceValidationError as e:
        context = GetMatchesResponse(match_filters=match_filters, error=e.message)

    return renderer.render_template(
        template_name="matches.html",
        context={**context.model_dump()},
        start_response=start_response,
    )
