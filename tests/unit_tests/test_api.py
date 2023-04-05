import copy

import pytest
from fastapi import status

from app.config import config

from .data.data import (
    LOGIN_HAPPY_CASE,
)

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

TEST_DATA_PATH = "database.json"


@pytest.mark.parametrize(
    "data, status_code, expectation_response",
    [
        (
            LOGIN_HAPPY_CASE["request"],
            status.HTTP_200_OK,
            LOGIN_HAPPY_CASE["response"],
        )
    ],
)
async def test_api_login(
    client, records, data, status_code, expectation_response
):
    patients, users = await records(TEST_DATA_PATH)
    response = await client.post(f"{config.OPENAPI_PREFIX}/users/login", json=data)
    assert response.status_code == status_code
    if expectation_response is not None:
        assert response.json() == expectation_response
