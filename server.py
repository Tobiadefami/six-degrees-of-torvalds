from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from find_connection import find_connection
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from load_cache import load_cache


app = FastAPI()
origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserRequest(BaseModel):
    username: str


@app.post("/search/{username}")
async def search_user(user_request: UserRequest):
    # Simulating an asynchronous call to find connections
    connection = await find_connection([(user_request.username, None)])
    return connection


@app.get("/{username}", response_model=UserRequest)
async def get_user(username: str):
    db = load_cache()
    if username in db:
        return db[username]
    else:
        return {"error": "User not found"}


# @app.post("/search/{user_id}")
# async def search_user(user_id: str):
#     start_state = [(user_id, None)]
#     connection = await find_connection(start_state)
# return connection


# @app.get("/{user_id}")
# async def search_user(user_id: str):
#     return FileResponse("/static/search.html")


# app.mount("/", StaticFiles(directory="static", html=True), name="static")
