from fastapi import FastAPI

from app.apis import users
from app.config import config


def configure_routes(app: FastAPI):
    app.include_router(router=users.router, prefix=config.OPENAPI_PREFIX)
