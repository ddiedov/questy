from pydantic import BaseModel
from app.quest_runs.model import QuestRun
from app.quest_structure.model import QuestStep
from app.quests.model import QuestForRuntimeView
from enum import Enum


class QuestRunUIState(str, Enum):
    IDLE = "idle"
    WRONG = "wrong"
    CORRECT_REVEAL = "correct_reveal"
    COMPLETED = "completed"


class QuestRunRuntimeView(BaseModel):
    run: QuestRun
    quest: QuestForRuntimeView | None = None
    current_step: QuestStep | None
    previous_steps: list[QuestStep]
    ui_state: QuestRunUIState = QuestRunUIState.IDLE
    message: str | None = None


class StepStateBuilder:
    @staticmethod
    def wrong(view: QuestRunRuntimeView, message: str):
        view.ui_state = QuestRunUIState.WRONG
        view.message = message
        return view
    @staticmethod
    def correct_reveal(view: QuestRunRuntimeView):
        view.ui_state = QuestRunUIState.CORRECT_REVEAL
        return view
    @staticmethod
    def completed(view: QuestRunRuntimeView):
        view.ui_state = QuestRunUIState.COMPLETED
        return view
    @staticmethod
    def idle(view: QuestRunRuntimeView):
        view.ui_state = QuestRunUIState.IDLE
        view.message = None
        return view