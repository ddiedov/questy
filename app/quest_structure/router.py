import logging

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from app.core.templates import templates
from app.core.router_factory import create_crud_router

from app.core.services_factory import (
    get_quest_structure_service,
    get_quest_structure_query_service,
    get_tasks_service,
    get_tasks_query_service
)

from app.tasks.filter import TasksFilter
from app.tasks.model import TaskCreate
from app.core.auth import build_user_dependency


logger = logging.getLogger(__name__)


router = create_crud_router(
    command_service=get_quest_structure_service(),
    query_service=get_quest_structure_query_service(),
    prefix="/quest-structure",
    require_auth_for_write=True,
    require_auth_for_read=False
)


get_user_for_write = build_user_dependency(True)

quest_tasks_router = APIRouter()


@quest_tasks_router.get("/quests/{quest_id}/tasks/add")
async def add_task_page(
    request: Request,
    quest_id: int,
    user_id=Depends(get_user_for_write)
):
    return templates.TemplateResponse(
        name="tasks/add.html",
        request=request,
        context={
            "quest_id": quest_id,
            "url": f"/quests/{quest_id}/tasks/create",
            "item": None,

            "page_title": "Create Task",
            "page_description": "Add a new step to your quest",

            "submit_label": "Create Task",

            "back_url": f"/quests/{quest_id}/edit",
            "cancel_url": f"/quests/{quest_id}/edit",
        }
    )


@quest_tasks_router.post("/quests/{quest_id}/tasks/create")
async def create_task_for_quest(
    request: Request,
    quest_id: int,
    user_id=Depends(get_user_for_write)
):
    form = await request.form()

    data_dict = dict(form)

    logger.debug("Create task for quest %s form data: %s", quest_id, data_dict)

    data = TaskCreate(**data_dict)

    task = get_tasks_service().create(
        data,
        user_id=user_id
    )

    logger.debug("Link task %s to quest %s", task.id, quest_id)

    get_quest_structure_service().add_task(
        quest_id=quest_id,
        task_id=task.id
    )

    return RedirectResponse(
        url=f"/quests/{quest_id}/edit",
        status_code=303
    )


@quest_tasks_router.get("/quests/{quest_id}/tasks/select")
async def select_task_page(
    request: Request,
    quest_id: int,
    user_id=Depends(get_user_for_write)
):
    filters = TasksFilter()

    tasks = get_tasks_query_service().list(
        filters=filters,
        current_user_id=user_id
    )

    quest_structure = get_quest_structure_query_service().get_by_quest(
        quest_id=quest_id,
        current_user_id=user_id
    )

    excluded_ids = [
        item.task.id
        for item in quest_structure.steps
    ]

    tasks = [
        task for task in tasks
        if task.id not in excluded_ids
    ]

    logger.debug("Selectable tasks for quest %s: %s", quest_id, tasks)

    return templates.TemplateResponse(
        name="tasks/list.html",
        request=request,
        context={
            "items": tasks,
            "quest_id": quest_id
        }
    )


@quest_tasks_router.post("/quests/{quest_id}/tasks/{task_id}/remove")
async def remove_task_from_quest(
    request: Request,
    quest_id: int,
    task_id: int,
    user_id=Depends(get_user_for_write)
):
    logger.debug("Task deletion from quest %s: %s", quest_id, task_id)

    get_quest_structure_service().remove_task(
        quest_id=quest_id,
        task_id=task_id
    )

    request.session["flash"] = "Task succesfully removed from quest"

    return RedirectResponse(
        url=f"/quests/{quest_id}/edit",
        status_code=303
    )


@quest_tasks_router.post("/quests/{quest_id}/tasks/reorder")
async def reorder_tasks(
    quest_id: int,
    payload: dict,
    user_id=Depends(get_user_for_write)
):
    get_quest_structure_service().reorder_tasks(
        quest_id=quest_id,
        ordered_ids=payload.get("items", [])
    )

    return {"success": True}