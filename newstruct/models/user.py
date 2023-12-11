import json
from datetime import datetime
from typing import Any, List, Optional

from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    email: str
    age: int
    created_on: datetime
    updated_on: datetime | None

    def to_response(self) -> dict[str, Any]:
        return json.loads(self.model_dump_json())


class UserList(BaseModel):
    users: List[User]


class UserCreateValidation(BaseModel):
    email: str
    age: int
