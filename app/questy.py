
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.core.templates import templates

from app.teams.router import router as teams_router
from app.quests.router import router as quests_router
from app.quest_applications.router import router as quest_applications_router


from app.teams.api import router as teams_api_router
from app.quests.api import router as quests_api_router
from app.quest_applications.api import router as quest_applications_api_router


from app.quests.service import QuestsService
quests_service = QuestsService()

app = FastAPI(title="Questy")

app.mount("/static", StaticFiles(directory="app/static"), name="static")

from app.core.auth_routers import create_auth_router
app.include_router(create_auth_router(""))

from app.core.auth import AuthMiddleware
app.add_middleware(AuthMiddleware)

app.include_router(teams_router)
app.include_router(quests_router)
app.include_router(quest_applications_router)

app.include_router(teams_api_router)
app.include_router(quest_applications_api_router)

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    featured_quests = quests_service.get_featured()
    return templates.TemplateResponse(
        "landing/landing.html",
        {
            "request": request,
            "featured_quests": featured_quests
        }
    )
