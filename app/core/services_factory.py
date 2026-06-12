from app.teams.service import TeamsService
from app.profiles.service import ProfilesService
from app.quests.service import QuestsService
from app.quest_applications.service import QuestApplicationsService
from app.quest_structure.service import QuestStructureService
from app.tasks.service import TasksService
from app.quest_runs.service import QuestRunsService

from app.queries.quests_query_service import QuestsQueryService
from app.queries.profiles_query_service import ProfilesQueryService
from app.queries.quest_applications_query_service import QuestApplicationsQueryService
from app.queries.quest_runs_query_service import QuestRunsQueryService
from app.queries.quest_runs_ui_query_service import QuestRunsUIQueryService
from app.queries.quest_structure_query_service import QuestStructureQueryService
from app.queries.tasks_query_service import TasksQueryService
from app.queries.teams_query_service import TeamsQueryService


# =========================
# DOMAIN SERVICES
# =========================

def get_teams_service():
    return TeamsService()


def get_profiles_service():
    return ProfilesService()


def get_quest_applications_service():
    return QuestApplicationsService()


def get_tasks_service():
    return TasksService()


def get_quest_structure_service():
    return QuestStructureService()


def get_quest_runs_service():
    return QuestRunsService(
        quest_runs_query_service = get_quest_runs_query_service(),
        quest_runs_ui_query_service = get_quest_runs_ui_query_service(),
        quest_structure_query_service=get_quest_structure_query_service(),
        tasks_service=get_tasks_service(),
        quests_query_service=get_quests_query_service(),
        quest_applications_service=get_quest_applications_service()
    )


def get_quests_service():
    return QuestsService()


# =========================
# QUERY SERVICES
# =========================

def get_teams_query_service():
    return TeamsQueryService()


def get_profiles_query_service():
    return ProfilesQueryService()


def get_quest_applications_query_service():
    return QuestApplicationsQueryService()


def get_tasks_query_service():
    return TasksQueryService()


def get_quest_structure_query_service():
    return QuestStructureQueryService(
        tasks_query_service=get_tasks_query_service()
    )


def get_quest_runs_query_service():
    return QuestRunsQueryService(
        quest_structure_query_service = get_quest_structure_query_service(),
        tasks_service = get_tasks_service()
    )

def get_quest_runs_ui_query_service():
    return QuestRunsUIQueryService(
        quest_structure_query_service = get_quest_structure_query_service(),
        tasks_service = get_tasks_service(),
        quests_query_service=get_quests_query_service()
    )


def get_quests_query_service():
    return QuestsQueryService(
        #quests_service=get_quests_service(),
        quest_applications_query_service=get_quest_applications_query_service(),
        quest_runs_query_service=get_quest_runs_query_service(),
        quest_structure_query_service=get_quest_structure_query_service(),
        profiles_query_service=get_profiles_query_service()
    )