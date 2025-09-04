from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TodoBase(BaseModel):
    content: str
    due: datetime


class TodoCreate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    done: bool = False

    # Pydantic v2: prefer model_config with from_attributes=True instead of orm_mode
    model_config = ConfigDict(from_attributes=True)
