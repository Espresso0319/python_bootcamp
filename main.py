import uvicorn
from fastapi import Depends, FastAPI
from contextlib import asynccontextmanager
from typing import Annotated
import models
from database import engine
from dependencies import get_query_token
from routers import items, users, auth_users
from fastapi_and_logging import FastAPIIncomingLog

models.Base.metadata.create_all(bind=engine)

# lifespan function
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


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
