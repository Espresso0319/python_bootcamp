from functools import lru_cache
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI

from config import DotenvSettings
from dependencies import get_query_token

app = FastAPI(dependencies=[Depends(get_query_token)])


# settings
@lru_cache
def get_settings():
    return DotenvSettings()


@app.get("/")
def index():
    return "ok"


@app.get("/info", tags=["test"])
def get_info(settings: Annotated[DotenvSettings, Depends(get_settings)]):
    return {
        "app_name": settings.app_name,
        "admin_email": settings.admin_email,
        "items_per_user": settings.items_per_user,
    }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=5000)
