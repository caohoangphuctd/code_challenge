from fastapi import FastAPI

from app.apis import users, groups, patients
from app.config import config


def configure_routes(app: FastAPI):
    app.include_router(router=users.router, prefix=config.OPENAPI_PREFIX)
    app.include_router(router=groups.router, prefix=config.OPENAPI_PREFIX)
    app.include_router(router=patients.router, prefix=config.OPENAPI_PREFIX)
