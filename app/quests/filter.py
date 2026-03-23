from pydantic import BaseModel


class QuestsFilter(BaseModel):

    featured: bool | None = None
    author_id: int | None = None