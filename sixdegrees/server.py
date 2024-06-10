import logging
import os

# from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from httpx import AsyncClient
from starlette.middleware.sessions import SessionMiddleware

from sixdegrees.custom_rate_limiter import is_rate_limited
from sixdegrees.find_connection import find_connection

# load_dotenv()

app = FastAPI()

GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
SECRET_KEY = os.getenv("SECRET_KEY")
BACKEND_HOST = os.getenv("BACKEND_HOST")
FRONTEND_HOST = os.getenv("FRONTEND_HOST")
REDIRECT_URI = f"http://{BACKEND_HOST}/callback"

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://github.com/login/oauth/authorize",
    tokenUrl="https://github.com/login/oauth/access_token",
)


origins = [f"http://{FRONTEND_HOST}"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/search/{username}")
async def search_user(username: str, request: Request):
    logging.debug("Request session data: %s", request.session)
    print("access token", request.session.get("access_token"))
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")

    user_id = user["id"]
    if is_rate_limited(user_id):
        raise HTTPException(
            status_code=429, detail="Rate limit exceeded. Try again later."
        )

    connection = await find_connection(
        [(username, None)], access_token=request.session["access_token"]
    )
    return connection


@app.get("/login")
def login():
    github_authorize_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=read:user,repo"
    )
    return RedirectResponse(github_authorize_url)


@app.get("/callback")
async def callback(request: Request, code: str):
    logging.debug("Callback endpoint hit with code: %s", code)
    async with AsyncClient() as client:
        token_response = await client.post(
            "https://github.com/login/oauth/access_token",
            headers={"Accept": "application/json"},
            data={
                "client_id": GITHUB_CLIENT_ID,
                "client_secret": GITHUB_CLIENT_SECRET,
                "code": code,
                "redirect_uri": REDIRECT_URI,
            },
        )
        token_response.raise_for_status()
        tokens = token_response.json()
        access_token = tokens.get("access_token")
        if not access_token:
            raise HTTPException(
                status_code=400, detail="Failed to retrieve access token"
            )

        # Store the access token in the session
        request.session["access_token"] = access_token
        logging.debug("Session access token set:", request.session["access_token"])
        # Retrieve user information
        user_response = await client.get(
            "https://api.github.com/user",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_response.raise_for_status()
        user = user_response.json()

        # Store the user information in the session
        request.session["user"] = user
        logging.debug("Session user set:", request.session["user"])
        print("user set in session", request.session["user"])
        # Redirect to the home page
        return RedirectResponse(url=f"http://{FRONTEND_HOST}")


@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url=f"http://{FRONTEND_HOST}")


@app.get("/user")
def get_user(request: Request):
    print(request.session)
    user = request.session.get("user")

    if not user:
        raise HTTPException(status_code=401, detail="User not authenticated")
    return JSONResponse(user)


app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY)
