import bcrypt
from pydantic import BaseModel, ConfigDict, Field, computed_field


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    @computed_field  # type: ignore[misc]
    @property
    def password_salt(self) -> bytes:
        if not hasattr(self, "_salt"):
            self._salt = bcrypt.gensalt()
        return self._salt

    @computed_field  # type: ignore[misc]
    @property
    def password_hash(self) -> bytes:
        b_password = self.password.encode("utf-8")
        hashed_password = bcrypt.hashpw(b_password, self.password_salt)
        return hashed_password


class UserUpdate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    username: str | None = Field()
    email: str | None = None


class User(BaseModel):
    user_id: int
    username: str
    email: str
    password_hash: bytes = Field(exclude=True)
    password_salt: bytes = Field(exclude=True)


class UserList(BaseModel):
    users: list[User]
