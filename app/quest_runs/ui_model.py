from pydantic import BaseModel
from app.quest_runs.model import QuestRun
from app.quest_structure.model import QuestStep
from app.quests.model import QuestForRuntimeView


class QuestRunRuntimeView(BaseModel):
    run: QuestRun
    quest: QuestForRuntimeView | None = None
    current_step: QuestStep | None
    previous_steps: list[QuestStep]