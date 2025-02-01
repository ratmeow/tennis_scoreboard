from src.endpoints.match import router as match_router
from src.server.middlewares import CORSMiddleware, log_request_middleware
from src.server.wsgi import WSGIApp

app = WSGIApp(router=match_router, static_dir="src/frontend")

app.add_middleware(CORSMiddleware)
app.add_middleware(log_request_middleware)
