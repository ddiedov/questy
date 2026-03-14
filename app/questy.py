
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

from app.teams.router import router as teams_router
from app.quests.router import router as quests_router

from app.quests.api import router as quests_api_router

app = FastAPI(title="Questy")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(quests_router)
app.include_router(teams_router)

app.include_router(quests_api_router)

@app.get("/")
def index():
    return RedirectResponse("/quests/")
