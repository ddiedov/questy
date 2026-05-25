import logging

from app.core.base_service import BaseService
from app.quest_runs.repository import QuestRunsRepository
from .model import QuestRun, QuestRunCreate, QuestRunUpdate, QuestRunPatch, QuestRunRuntimeView, QuestRunStatusType
from .filter import QuestRunsFilter

logger = logging.getLogger(__name__)


class QuestRunsService(BaseService):
    repository = QuestRunsRepository()

    model = QuestRun
    create_model = QuestRunCreate
    update_model = QuestRunUpdate
    patch_model = QuestRunPatch

    def __init__(self, quest_structure_service, tasks_service):
        super().__init__()
        self.quest_structure_service = quest_structure_service
        self.tasks_service = tasks_service 


    # =========================
    # RUNTIME VIEW
    # =========================
    def get(self, id: int) -> QuestRunRuntimeView | None:
        run = super().get(id)
        if not run:
            return None

        structure = self.quest_structure_service.get_by_quest(run.quest_id)

        tasks = structure.tasks if structure else []

        # если задач нет — безопасный early return
        if not tasks:
            return QuestRunRuntimeView(
                run=run,
                current_task=None,
                previous_tasks=[]
            )

        # ищем индекс текущей задачи безопасно
        current_index = None

        if run.current_task_id is not None:
            current_index = next(
                (i for i, t in enumerate(tasks) if t.id == run.current_task_id),
                None
            )

        # fallback — старт с начала
        if current_index is None:
            current_index = 0

        current_task = tasks[current_index]

        previous_tasks = tasks[:current_index]

        return QuestRunRuntimeView(
            run=run,
            current_task=current_task,
            previous_tasks=previous_tasks
        )

    # =========================
    # START RUN
    # =========================
    def start_run(self, quest_id: int, participant_id: str):
        existing = self.get_active_run(
            quest_id=quest_id,
            participant_id=participant_id
        )

        if existing:
            return existing

        structure = self.quest_structure_service.get_by_quest(quest_id)
        tasks = structure.tasks if structure else []

        first_task_id = tasks[0].id if tasks else None

        return self.create(
            QuestRunCreate(
                quest_id=quest_id,
                participant_id=participant_id,
                current_task_id=first_task_id
            ),
            participant_id
        )

    # =========================
    # ACTIVE RUN
    # =========================
    def get_active_run(self, quest_id: int, participant_id: str):
        runs = self.list(
            filters=QuestRunsFilter(
                quest_id=quest_id,
                participant_id=participant_id,
                status=QuestRunStatusType.ACTIVE.value
            )
        )

        return runs[0] if runs else None
    
    def get_run_state(self, quest_id: int, participant_id: str):
        active = self.get_active_run(quest_id, participant_id)

        if active:
            return {
                "state": "resume",
                "run_id": active.id
            }

        return {
            "state": "start",
            "run_id": None
        }
    


    # =========================
    # ANSWER
    # =========================
    def submit_answer(
        self,
        run_id: int,
        answer: str,
        participant_id: str
    ):
        run = super().get(run_id)

        if not run:
            return {
                "success": False,
                "state": "wrong",
                "message": "Run not found"
            }

        structure = self.quest_structure_service.get_by_quest(run.quest_id)
        tasks = structure.tasks if structure else []

        current_index = next(
            (i for i, t in enumerate(tasks) if t.id == run.current_task_id),
            None
        )

        if current_index is None:
            return {
                "success": False,
                "state": "wrong",
                "message": "Current task not found"
            }

        current_item = tasks[current_index]
        current_task = current_item.task

        success, error = self.tasks_service.validate_answer(
            current_task,
            answer
        )

        # ❌ WRONG ANSWER
        if not success:
            return {
                "success": False,
                "state": "wrong",
                "message": error
            }

        next_index = current_index + 1

        # 🏁 COMPLETED
        if next_index >= len(tasks):
            self.patch(
                run_id,
                QuestRunPatch(
                    current_task_id=None,
                    status=QuestRunStatusType.COMPLETED
                )
            )

            return {
                "success": True,
                "state": "completed",
                "message": None
            }

        # ➡️ CORRECT (NEXT TASK)
        next_task_id = tasks[next_index].id

        self.patch(
            run_id,
            QuestRunPatch(
                current_task_id=next_task_id
            )
        )

        return {
            "success": True,
            "state": "correct",
            "message": None
        }