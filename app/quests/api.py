from fastapi import APIRouter, HTTPException

from .service import QuestsService
from .model import Quest, QuestCreate, QuestUpdate


router = APIRouter(
    prefix="/api/quests",
    tags=["quests"]
)

service = QuestsService()


@router.get("/", response_model=list[Quest])
def list_quests():

    return service.list()


@router.get("/{id}", response_model=Quest)
def get_quest(id: int):

    quest = service.get(id)

    if not quest:
        raise HTTPException(status_code=404)

    return quest


@router.post("/", response_model=Quest)
def create_quest(data: QuestCreate):

    return service.create(data)


@router.put("/{id}", response_model=Quest)
def update_quest(id: int, data: QuestUpdate):

    quest = service.update(id, data)

    if not quest:
        raise HTTPException(status_code=404)

    return quest