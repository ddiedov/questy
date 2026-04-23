from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from app.core.templates import templates
from app.core.router_factory import create_crud_router
from app.core.services_factory import get_quest_structure_service, get_tasks_service
from app.tasks.filter import TasksFilter
from app.tasks.model import TaskCreate
from app.core.auth import build_user_dependency



router = create_crud_router(
    get_quest_structure_service(),
    "/quest-structure",
    True,
    False
)


get_user_for_write = build_user_dependency(True)

quest_tasks_router = APIRouter()

@quest_tasks_router.get("/quests/{quest_id}/tasks/add")
async def add_task_page(
    request: Request,
    quest_id: int,
    user_id = Depends(get_user_for_write)
):
    return templates.TemplateResponse(
        "tasks/add.html",
        {
            "request": request,
            "quest_id": quest_id,
            "url": f"/quests/{quest_id}/tasks/create"
        }
    )

@quest_tasks_router.post("/quests/{quest_id}/tasks/create")
async def create_task_for_quest(
    request: Request,
    quest_id: int,
    user_id = Depends(get_user_for_write)
):
    form = await request.form()
    data_dict = dict(form)
    print (data_dict)
    data = TaskCreate(**data_dict)

    task = get_tasks_service().create(data, user_id=user_id)
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
    user_id = Depends(get_user_for_write)
):
    filters = TasksFilter()
#    filters.quest_id = quest_id  # 👈 ок, если ты реально фильтруешь “не добавленные”
    print(filters)

    tasks = get_tasks_service().list(
        filters=filters,
        current_user_id=user_id
    )
    print(tasks)

    return templates.TemplateResponse(
        "tasks/list.html",
        {
            "request": request,
            "items": tasks,
            "quest_id": quest_id
        }
    )
