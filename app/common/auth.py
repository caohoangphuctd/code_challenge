import re
import logging
import json
from redis.asyncio import Redis

from fastapi.params import Depends
from fastapi.security import HTTPBearer
from fastapi_jwt_auth import AuthJWT

from app.config import config
from app.database.depends import get_redis_db
from app.exceptions.configure_exceptions import (
    ErrorInvalidTokenException, ErrorRequestException
)
from app.database.redis import RedisSession


logger = logging.getLogger("default")

OAUTH2_TOKEN = HTTPBearer(
    auto_error=False
)


@AuthJWT.load_config
def get_config():
    return config.jwt_config


async def depend_admin_access_token(
    authorize: AuthJWT = Depends(),
    _oauth2_schema: str = Depends(OAUTH2_TOKEN)
):
    raw_data = await verify_access_token(authorize, "users")
    if raw_data["is_admin"] is False:
        raise ErrorInvalidTokenException()
    return raw_data


# def depend_user_refresh_token(
#     authorize: AuthJWT = Depends(),
#     _oauth2_schema: str = Depends(OAUTH2_TOKEN)
# ):
#     return verify_refresh_token(authorize, "users")


def generate_key_auth_token(raw_jwt):
    return f"/{config.redis_config.redis_prefix}/auth/{raw_jwt['sub']}/{raw_jwt['id']}/{raw_jwt['type']}_token"


def get_key_auth_token(user_id):
    return f"/{config.redis_config.redis_prefix}/auth/users/{user_id}/access_token"


async def check_existing_jwt_token(raw_jwt):
    entry = await RedisSession.get(generate_key_auth_token(raw_jwt))
    return entry is not None


async def verify_access_token(authorize, sub):
    try:
        authorize.jwt_required()
        raw_jwt = authorize.get_raw_jwt()
        if authorize.get_jwt_subject() == sub and await check_existing_jwt_token(raw_jwt):
            return raw_jwt
    except Exception as e:
        logger.info(e)
    raise ErrorInvalidTokenException()


# def verify_refresh_token(authorize, sub):
#     try:
#         authorize.jwt_refresh_token_required()
#         raw_jwt = authorize.get_raw_jwt()
#         if authorize.get_jwt_subject() == sub and check_existing_jwt_token(raw_jwt):
#             return raw_jwt
#     except Exception as e:
#         logger.info(e)
#     raise ErrorRequestException(INVALID_REFRESH_TOKEN)


async def get_jwt_claims(**kwargs):
    return {
        "sub": kwargs.get('sub', None),
        "id": kwargs.get('id', None),
        "is_admin": kwargs.get('is_admin', None)
    }


async def create_redis_data_for_login(
    auth_jwt,
    access_token: str = None,
    refresh_token: str = None
):
    try:
        redis = RedisSession
        if access_token is not None:
            data = {"access_token": access_token, "refresg_token": refresh_token}
            raw_jwt_access = auth_jwt.get_raw_jwt(access_token)
            if refresh_token is not None:
                raw_jwt_refresh = auth_jwt.get_raw_jwt(refresh_token)
                await redis.set(
                    generate_key_auth_token(raw_jwt_refresh),
                    json.dumps(data)
                )
                data['jwt_refresh'] = raw_jwt_refresh['jti']
            await redis.setex(
                generate_key_auth_token(raw_jwt_access),
                config.jwt_config.authjwt_access_token_expires,
                json.dumps(data)
            )
    except Exception as e:
        raise ErrorRequestException(e.__str__())


# def create_redis_data_for_refresh_token(
#     auth_jwt,
#     access_token: str = None,
#     refresh_jti: str = None
# ):
#     try:
#         raw_jwt_access = auth_jwt.get_raw_jwt(access_token)
#         data = {
#             'jwt_refresh': refresh_jti
#         }
#         REDIS_CONN.setex(
#             generate_key_auth_token(raw_jwt_access),
#             raw_jwt_access['exp'],
#             json.dumps(data)
#         )
#     except Exception as e:
#         raise_exception(e)


async def create_auth_tokens(
    auth_jwt,
    claims: dict
):
    access_expires_time = config.jwt_config.authjwt_access_token_expires
    refresh_token = auth_jwt.create_refresh_token(
        subject=claims['sub'],
        user_claims=claims,
        expires_time=False
    )
    access_token = auth_jwt.create_access_token(
        subject=claims['sub'],
        user_claims=claims,
        expires_time=access_expires_time
    )
    await create_redis_data_for_login(
        auth_jwt,
        access_token=access_token,
        refresh_token=refresh_token
    )
    return access_token, refresh_token


# def refresh_user_token(
#     authorize: dict
# ):
#     claims = get_jwt_claims(
#         sub="users",
#         id=authorize.get("id")
#     )
#     auth_jwt = AuthJWT()
#     access_expires_time = config.jwt_config.authjwt_access_token_expires
#     access_token = auth_jwt.create_access_token(
#         subject=claims['sub'],
#         user_claims=claims,
#         expires_time=access_expires_time
#     )
#     create_redis_data_for_refresh_token(
#         auth_jwt=auth_jwt,
#         access_token=access_token,
#         refresh_jti=authorize.get("jti")
#     )
#     return access_token


async def create_user_token(
    user_id: int,
    is_admin: bool = False
):
    redis: Redis = RedisSession
    key = get_key_auth_token(user_id)
    data = await redis.get(key)
    if data:
        tokens = json.loads(data)
        return tokens["access_token"], tokens["refresg_token"]
    claims = await get_jwt_claims(
        sub="users",
        id=user_id,
        is_admin=is_admin
    )
    auth_jwt = AuthJWT()
    return await create_auth_tokens(
        auth_jwt=auth_jwt,
        claims=claims
    )


# def logout_process(
#         authorize: dict
# ):
#     try:
#         data_redis = REDIS_CONN.get(generate_key_auth_token(authorize))
#         if data_redis:
#             data = json.loads(data_redis)
#             REDIS_CONN.delete(generate_key_auth_token(authorize))
#             authorize['type'] = "refresh"
#             authorize['jti'] = data['jwt_refresh']
#             REDIS_CONN.delete(generate_key_auth_token(authorize))
#     except Exception as e:
#         raise_exception(e)
