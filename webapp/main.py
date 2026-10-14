import base64
from typing import Union
from os.path import dirname, abspath, join
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from .services import TokenService, UserService
from .repos import UserRepo
from . import schemas

current_dir = dirname(abspath(__file__))
static_path = join(current_dir, "static")

app = FastAPI()
app.mount("/ui", StaticFiles(directory=static_path), name="ui")


class Body(BaseModel):
    length: Union[int, None] = 20


# Application-wide repository (file-based SQLite)
_repo = UserRepo(db_path="data.db")


@app.on_event("startup")
def startup_event():
    _repo.init_db()


# Dependency providers
def get_token_service() -> TokenService:
    return TokenService()


def get_user_repo() -> UserRepo:
    return _repo


def get_user_service(repo: UserRepo = Depends(get_user_repo)) -> UserService:
    return UserService(repo)


@app.get('/')
def root():
    html_path = join(static_path, "index.html")
    return FileResponse(html_path)


@app.get('/ping')
def ping():
    return {'status': 'ok'}


@app.post('/generate')
def generate(body: Body, token_service: TokenService = Depends(get_token_service)):
    """
    Generate a pseudo-random token ID of twenty characters by default. Example POST request body:

    {
        "length": 20
    }
    """
    string = token_service.generate(body.length)
    return {'token': string}


# User CRUD endpoints
@app.post('/users', status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, user_service: UserService = Depends(get_user_service)):
    created = user_service.create_user(user)
    return created


@app.get('/users/{user_id}')
def get_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    user = user_service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user


@app.put('/users/{user_id}')
def update_user(user_id: int, user_update: schemas.UserUpdate, user_service: UserService = Depends(get_user_service)):
    updated = user_service.update_user(user_id, user_update)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return updated


@app.delete('/users/{user_id}')
def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    deleted = user_service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return {'deleted': True}