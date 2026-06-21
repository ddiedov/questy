import logging

from app.core.base_command_service import BaseCommandService
from app.quest_runs.repository import QuestRunsRepository
from .model import QuestRun, QuestRunCreate, QuestRunUpdate, QuestRunPatch, QuestRunStatusType

from app.queries.quest_runs_ui_query_service import QuestRunsUIQueryService

from fastapi import HTTPException

logger = logging.getLogger(__name__)


class QuestRunsService(BaseCommandService):
    repository = QuestRunsRepository()

    model = QuestRun
    create_model = QuestRunCreate
    update_model = QuestRunUpdate
    patch_model = QuestRunPatch

    def __init__(self, 
                 quest_runs_ui_query_service: QuestRunsUIQueryService, 
                 quest_structure_query_service, 
                 tasks_service, 
                 quests_query_service, 
                 quest_applications_service
                ):
        super().__init__()
        self.quest_runs_ui_query_service = quest_runs_ui_query_service
        self.quest_structure_query_service = quest_structure_query_service
        self.tasks_service = tasks_service 
        self.quests_query_service = quests_query_service
        self.quest_applications_service = quest_applications_service

  
    # =========================
    # START RUN
    # =========================
    def start_run(self, quest_id: int, participant_id: str):
        if not self.quests_query_service.can_start(quest_id, participant_id):
            raise HTTPException(403)

        first_step = (
            self.quest_structure_query_service.get_first_step(
                quest_id
            )
        )
        
        first_step_id = (
            first_step.id
            if first_step
            else None
        )

        run = self.create(
            QuestRunCreate(
                quest_id=quest_id,
                participant_id=participant_id,
                current_step_id=first_step_id
            ),
            participant_id
        )
        
        self.quest_applications_service.mark_used(
            quest_id=quest_id,
            participant_id=participant_id
        )

        return run

  


    # =========================
    # ANSWER
    # =========================
    def submit_answer(
        self,
        run_id: int,
        answer: str,
        participant_id: str
    ):
        run_view = self.quest_runs_ui_query_service.get(run_id)

        if not run_view:
            return {
                "success": False,
                "state": "wrong",
                "message": "Run not found"
            }

        run = run_view.run

        if not run_view.current_step:
            return {
                "success": False,
                "state": "wrong",
                "message": "Current task not found"
            }

        current_task = run_view.current_step.task

        success, error = self.tasks_service.validate_answer(
            current_task,
            answer
        )

        # WRONG ANSWER
        if not success:
            return {
                "success": False,
                "state": "wrong",
                "message": error
            }

        # =========================
        # CURRENT POSITION LOGIC
        # =========================
        current_position = self.quest_structure_query_service.get_step_position(
            run.quest_id,
            run.current_step_id
        )
        completed_step_id = run.current_step_id

        structure = self.quest_structure_query_service.get_by_quest(run.quest_id)
        steps = structure.steps if structure else []

        next_index = current_position + 1

        # =========================
        # COMPLETED
        # =========================
        if next_index >= len(steps):
            self.patch(
                run_id,
                QuestRunPatch(
                    current_step_id=None,
                    status=QuestRunStatusType.COMPLETED
                )
            )

            return {
                "success": True,
                "state": "completed",
                "message": None,
                "expanded_step_id": completed_step_id
            }

        # =========================
        # NEXT STEP
        # =========================
        next_step_id = steps[next_index].id

        self.patch(
            run_id,
            QuestRunPatch(
                current_step_id=next_step_id
            )
        )

        return {
            "success": True,
            "state": "correct",
            "message": None,
            "expanded_step_id": completed_step_id
        }