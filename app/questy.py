
import logging

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.core.templates import templates

from app.teams.router import router as teams_router
from app.profiles.router import router as profiles_router
from app.quests.router import router as quests_router
from app.quest_applications.router import router as quest_applications_router
from app.quest_applications.router import quest_applications_router as application_actions_router
from app.tasks.router import router as tasks_router

from app.quest_structure.router import router as quest_structure_router
from app.quest_structure.router import quest_tasks_router as quest_tasks_router

from app.teams.api import router as teams_api_router
from app.quests.api import router as quests_api_router
from app.quest_applications.api import router as quest_applications_api_router
from app.tasks.api import router as tasks_api_router

from app.quest_runs.router import router as quest_runs_router
from app.quest_runs.router import quest_runs_router as quest_runs_router_extensions

from config import SESSION_SECRET

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s:%(name)s:%(message)s"
)

# App logs
logger = logging.getLogger(__name__)

# Reduce noisy third-party logs
logging.getLogger("hpack").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("asyncio").setLevel(logging.WARNING)
logging.getLogger("python_multipart").setLevel(logging.WARNING)

app = FastAPI(title="Questy")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

from app.core.auth_routers import create_auth_router
app.include_router(create_auth_router("/auth"))

from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

from app.core.auth import AuthMiddleware
app.add_middleware(AuthMiddleware)

app.include_router(teams_router)
app.include_router(profiles_router)
app.include_router(quests_router)
app.include_router(quest_applications_router)
app.include_router(application_actions_router)
app.include_router(tasks_router)

app.include_router(quest_structure_router)
app.include_router(quest_tasks_router)

app.include_router(quest_runs_router)
app.include_router(quest_runs_router_extensions)

app.include_router(teams_api_router)
app.include_router(quests_api_router)
app.include_router(quest_applications_api_router)
app.include_router(tasks_api_router)

from app.core.services_factory import get_quests_query_service
quests_query_service = get_quests_query_service()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    user = getattr(request.state, "user", None)
    featured_quests = quests_query_service.get_featured(user.id if user else None)

    logger.debug("Templates type: %s", type(templates))
    logger.debug("Featured quests type: %s", type(featured_quests))
    logger.debug("Landing template type: %s", type("landing/landing.html"))

    return templates.TemplateResponse(
        name = "landing/landing.html",
        request = request,
        context = {
            "featured_quests": featured_quests
        }
    )
