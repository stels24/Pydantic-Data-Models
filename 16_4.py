from fastapi import FastAPI, Path, status, Body, HTTPException
from typing import Annotated, List
from pydantic import BaseModel


app = FastAPI()

users = []

class User(BaseModel):
    id: int = None
    username: str
    age: int = None


@app.get("/users")
async def get_all_users() -> List[User]:
    return users


@app.post("/user/{user_name}/{age}", response_model=str)
async def create_user(user: User, user_name: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="Mikhail")],
        age: int = Path(ge=18, le=120, description="Enter age", example=60)) -> str:
    if users:
        current_index = max(user.id for user in users) + 1
    else:
        current_index = 1
    user.id = current_index
    user.username = user_name
    user.age = age
    users.append(user)
    return f"User {current_index} is registered"


@app.put("/user/{user_id}/{user_name}/{age}", response_model=str)
async def update_user(user: User, user_name: Annotated[str, Path(min_length=5, max_length=20, description="Enter username", example="Mikhail")],
        age: int = Path(ge=18, le=120, description="Enter age", example=60),
        user_id: int = Path(ge=1)) -> str:
    for existing_user in users:
        if existing_user.id == user_id:
            existing_user.username = user_name
            existing_user.age = age
            return f"The user {user_id} is updated."
    raise HTTPException(status_code=404, detail="Пользователь не найден.")



@app.delete("/user/{user_id}", response_model=str)
async def delete_user(user_id: int = Path(ge=1)) -> str:
    for index, existing_user in enumerate(users):
        if existing_user.id == user_id:
            users.pop(index)
            return f"Пользователь с ID {user_id} удален."

    raise HTTPException(status_code=404, detail="Пользователь не найден.")