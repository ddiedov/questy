from app.teams.service import TeamsService
from app.quests.service import QuestsService
from app.quest_applications.service import QuestApplicationsService
from app.quest_structure.service import QuestStructureService
from app.tasks.service import TasksService

def get_teams_service():
    return TeamsService()

def get_quest_applications_service():
    return QuestApplicationsService()

def get_tasks_service():
    return TasksService()

def get_quest_structure_service():
    return QuestStructureService(
        tasks_service = get_tasks_service()
    )

def get_quests_service():
    return QuestsService(
        quest_applications_service=get_quest_applications_service(),
        quest_tasks_service=get_quest_tasks_service()
    )
