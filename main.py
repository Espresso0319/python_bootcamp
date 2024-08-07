from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Annotated

import uvicorn
from fastapi import Cookie, Depends, FastAPI, Header, Request

import models
from config import Settings
from database import engine
from dependencies import get_query_token
from routers import items, users, auth_users
from fastapi_and_logging import FastAPIIncomingLog

models.Base.metadata.create_all(bind=engine)


# lifespan funciton
def fake_answer_to_everything_ml_model(x: float):
    return x * 42


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the ML model
    ml_models["answer_to_everything"] = fake_answer_to_everything_ml_model
    print("model loaded")
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()
    print("clean up")


app = FastAPI(dependencies=[Depends(get_query_token)], lifespan=lifespan)
FastAPIIncomingLog(app, log_path="./app.log")

abc = app

app.include_router(items.router)
app.include_router(users.router)
app.include_router(auth_users.router)

# --- deprecated event start ----
cache = {}


@app.on_event("startup")
async def startup_event():
    cache["foo"] = {"name": "Fighters"}
    cache["bar"] = {"name": "Tenders"}


@app.on_event("shutdown")
async def shutdown_event():
    cache.clear()


# ---- deprecated event end ----


# settings
@lru_cache
def get_settings():
    return Settings()


@app.get("/")
def index():
    return "ok"


@app.get("/no-type-hints/{query}", tags=["test"])
def no_type_hints(q, p=None):
    return {"q": q, "p": p}


@app.get("/header-test", tags=["test"])
def header_test(user_agent: Annotated[str | None, Header()] = None, x_token: Annotated[str, Header()] = None):
    return {"user_agent": user_agent, "x_token": x_token}


@app.get("/cookie-test", tags=["test", "cookie"])
def cookie_test(session_id: Annotated[str | None, Cookie()] = None, expires: Annotated[str | None, Cookie()] = None):
    return {"session_id": session_id, "Expires": expires}


@app.get("/full-req-obj", tags=["test"])
def full_req_obj_test(request: Request):
    return {"headers": request.headers, "cookies": request.cookies}


@app.get("/info", tags=["test"])
def get_info(settings: Annotated[Settings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
