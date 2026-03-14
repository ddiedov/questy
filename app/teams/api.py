from fastapi import APIRouter, HTTPException

from .service import TeamsService
from .model import Team, TeamCreate, TeamUpdate


router = APIRouter(
    prefix="/api/teams",
    tags=["teams"]
)

service = TeamsService()


@router.get("/", response_model=list[Team])
def list_teams():

    return service.list()


@router.get("/{id}", response_model=Team)
def get_teams(id: int):

    team = service.get(id)

    if not team:
        raise HTTPException(status_code=404)

    return team


@router.post("/", response_model=Team)
def create_team(data: TeamCreate):

    return service.create(data)


@router.put("/{id}", response_model=Team)
def update_team(id: int, data: TeamUpdate):

    team = service.update(id, data)

    if not team:
        raise HTTPException(status_code=404)

    return team