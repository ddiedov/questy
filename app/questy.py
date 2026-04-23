
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.core.templates import templates

from app.teams.router import router as teams_router
from app.quests.router import router as quests_router
from app.quest_applications.router import router as quest_applications_router
from app.tasks.router import router as tasks_router

from app.quest_structure.router import router as quest_structure_router
from app.quest_structure.router import quest_tasks_router as quest_tasks_router

from app.teams.api import router as teams_api_router
from app.quests.api import router as quests_api_router
from app.quest_applications.api import router as quest_applications_api_router
from app.tasks.api import router as tasks_api_router


app = FastAPI(title="Questy")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

from app.core.auth_routers import create_auth_router
app.include_router(create_auth_router(""))

import secrets
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware,secret_key=secrets.token_hex(32))

from app.core.auth import AuthMiddleware
app.add_middleware(AuthMiddleware)

app.include_router(teams_router)
app.include_router(quests_router)
app.include_router(quest_applications_router)
app.include_router(tasks_router)

app.include_router(quest_structure_router)
app.include_router(quest_tasks_router)

app.include_router(teams_api_router)
app.include_router(quests_api_router)
app.include_router(quest_applications_api_router)
app.include_router(tasks_api_router)

from app.core.services_factory import get_quests_service
quests_service = get_quests_service()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    user = getattr(request.state, "user", None)
    featured_quests = quests_service.get_featured(user.id if user else None)
    return templates.TemplateResponse(
        "landing/landing.html",
        {
            "request": request,
            "featured_quests": featured_quests
        }
    )
