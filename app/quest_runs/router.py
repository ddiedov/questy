import logging

from fastapi import APIRouter, Request, Depends, Form
from fastapi.responses import RedirectResponse

from app.core.templates import templates
from app.core.router_factory import create_crud_router
from app.core.services_factory import get_quest_runs_service
from app.core.auth import build_user_dependency


logger = logging.getLogger(__name__)


router = create_crud_router(
    get_quest_runs_service(),
    "/quest-runs",
    True,
    False
)

get_user_for_write = build_user_dependency(True)

quest_runs_router = APIRouter()


@quest_runs_router.get("/quests/{quest_id}/start")
async def start_quest_run(
    request: Request,
    quest_id: int,
    user_id=Depends(get_user_for_write)
):
    run = get_quest_runs_service().start_run(
        quest_id=quest_id,
        participant_id=user_id
    )

    return RedirectResponse(
        url=f"/quest-runs/{run.id}",
        status_code=303
    )


@quest_runs_router.post("/quest-runs/{run_id}/answer")
async def submit_answer(
    request: Request,
    run_id: int,
    answer: str = Form(...),
    user_id=Depends(get_user_for_write)
):
    service = get_quest_runs_service()

    result = service.submit_answer(
        run_id=run_id,
        answer=answer,
        participant_id=user_id
    )

    # -------------------------
    # WRONG ANSWER
    # -------------------------
    if result["state"] == "wrong":
        item = service.get(run_id)

        return templates.TemplateResponse(
            name="quest-runs/details.html",
            request=request,
            context={
                "item": item,
                "answer_state": "wrong",
                "message": result["message"]
            }
        )

    # -------------------------
    # COMPLETED
    # -------------------------
    if result["state"] == "completed":
        return RedirectResponse(
            url=f"/quest-runs/{run_id}",
            status_code=303
        )

    # -------------------------
    # CORRECT ANSWER (NEXT TASK)
    # -------------------------
    item = service.get(run_id)

    return templates.TemplateResponse(
        name="quest-runs/details.html",
        request=request,
        context={
            "item": item,
            "answer_state": "correct",
            "message": "Correct answer"
        }
    )