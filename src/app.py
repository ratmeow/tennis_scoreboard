from src.endpoints import player_router, match_router
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from src import templates

app = FastAPI()
app.include_router(player_router)
app.include_router(match_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/frontend"), name="static")


@app.get("/")
async def get_root(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})
