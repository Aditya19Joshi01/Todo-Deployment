from datetime import datetime
from typing import Optional
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


# --- User / Auth schemas ---
class UserCreate(BaseModel):
    username: str
    password: str


class User(BaseModel):
    id: int
    username: str
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    sub: Optional[str] = None
