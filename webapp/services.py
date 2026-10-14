import os
import base64
from typing import Union
from .repos import UserRepo
from .schemas import UserCreate, UserUpdate


class TokenService:
    def generate(self, length: Union[int, None] = 20) -> str:
        # generate a pseudo-random token using os.urandom and base64
        if length is None:
            length = 20
        string = base64.b64encode(os.urandom(64))[: length].decode("utf-8")
        return string


class UserService:
    def __init__(self, repo: UserRepo):
        self.repo = repo

    def create_user(self, user: UserCreate) -> dict:
        return self.repo.create_user(user.name, user.email)

    def get_user(self, user_id: int) -> dict:
        return self.repo.get_user(user_id)

    def update_user(self, user_id: int, user: UserUpdate) -> dict:
        return self.repo.update_user(user_id, user.name, user.email)

    def delete_user(self, user_id: int) -> bool:
        return self.repo.delete_user(user_id)
