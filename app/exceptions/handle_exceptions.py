import logging

from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse

from app.exceptions.configure_exceptions import (
    ItemDoesNotExist, BothEmailAndPhoneAreNone,
    ItemExist, ErrorRequestException,
    ErrorAuthenticationException
)

logger = logging.getLogger("default")


def configure_exceptions_handlers(app: FastAPI):
    @app.exception_handler(ErrorRequestException)
    async def handle_exception(
        request: Request, exc: ErrorRequestException
    ) -> ORJSONResponse:
        logger.error(exc, exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": False, "message": exc.__str__()},
        )

    @app.exception_handler(ItemExist)
    async def handle_item_exist(
        request: Request, exc: ItemExist
    ) -> ORJSONResponse:
        logger.error(exc, exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": False, "message": exc.__str__()},
        )

    @app.exception_handler(ItemDoesNotExist)
    async def handle_item_does_not_exist(
        request: Request, exc: ItemDoesNotExist
    ) -> ORJSONResponse:
        logger.error(exc, exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": False, "message": exc.__str__()},
        )

    @app.exception_handler(BothEmailAndPhoneAreNone)
    async def handle_both_email_and_phone_number_are_none(
        request: Request, exc: BothEmailAndPhoneAreNone
    ) -> ORJSONResponse:
        logger.error(exc, exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"status": False, "message": exc.__str__()},
        )

    @app.exception_handler(ErrorAuthenticationException)
    async def handle_authentication_error(
        request: Request, exc: ErrorAuthenticationException
    ) -> ORJSONResponse:
        logger.error(exc, exc_info=exc)
        return ORJSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"status": False, "message": exc.__str__()},
        )