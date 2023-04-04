import copy

import pytest
from fastapi import status

from app.config import config

from .data.data import (
    CREATE_APPLICANT_EXISTS,
    CREATE_APPLICANT_HAPPY_CASE,
    CREATE_JOB_HAPPY_CASE,
    CREATE_JOB_INVALID_FIELDS,
    CREATE_JOB_MISSING_FIELDS,
    CREATE_WORKER_HAPPY_CASE,
    CREATE_WORKER_INVALID_FIELDS,
    CREATE_WORKER_MISSING_FIELDS,
    CREATE_WORKER_WITH_WORKER_NOT_EXISTS,
    GET_JOB_RECOMMENDATION_HAPPY_CASE,
    GET_JOB_RECOMMENDATION_HAPPY_CASE_WITH_WORKER_NOT_EXISTS,
    GET_SEARCH_JOB_HAPPY_CASE,
    UPDATE_WORKER_HAPPY_CASE,
)

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio

TEST_DATA_PATH = "database.json"


@pytest.mark.parametrize(
    "data, status_code, expectation_response",
    [
        (
            CREATE_JOB_HAPPY_CASE["request"],
            status.HTTP_201_CREATED,
            CREATE_JOB_HAPPY_CASE["response"],
        ),
        (
            CREATE_JOB_MISSING_FIELDS["request"],
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            CREATE_JOB_MISSING_FIELDS["response"],
        ),
        (
            CREATE_JOB_INVALID_FIELDS["request"],
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            CREATE_JOB_INVALID_FIELDS["response"],
        ),
    ],
)
async def test_api_create_job(client, data, status_code, expectation_response):
    response = await client.post(f"{config.OPENAPI_PREFIX}/jobs", json=data)
    assert response.status_code == status_code
    if expectation_response is not None:
        assert response.json() == expectation_response


@pytest.mark.parametrize(
    "data, status_code, expectation_response",
    [
        (
            CREATE_WORKER_HAPPY_CASE["request"],
            status.HTTP_201_CREATED,
            CREATE_WORKER_HAPPY_CASE["response"],
        ),
        (
            CREATE_WORKER_MISSING_FIELDS["request"],
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            CREATE_WORKER_MISSING_FIELDS["response"],
        ),
        (
            CREATE_WORKER_INVALID_FIELDS["request"],
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            CREATE_WORKER_INVALID_FIELDS["response"],
        ),
    ],
)
async def test_api_create_worker(client, data, status_code, expectation_response):
    response = await client.post(f"{config.OPENAPI_PREFIX}/workers", json=data)
    assert response.status_code == status_code
    if expectation_response is not None:
        assert response.json() == expectation_response


@pytest.mark.parametrize(
    "data, status_code, expectation_response",
    [
        (
            CREATE_APPLICANT_HAPPY_CASE["request"],
            status.HTTP_201_CREATED,
            CREATE_APPLICANT_HAPPY_CASE["response"],
        ),
        (
            CREATE_APPLICANT_EXISTS["request"],
            status.HTTP_400_BAD_REQUEST,
            CREATE_APPLICANT_EXISTS["response"],
        ),
        (
            CREATE_WORKER_WITH_WORKER_NOT_EXISTS["request"],
            status.HTTP_404_NOT_FOUND,
            CREATE_WORKER_WITH_WORKER_NOT_EXISTS["response"],
        ),
    ],
)
async def test_api_create_applicant(
    client, records, data, status_code, expectation_response
):
    await records(TEST_DATA_PATH)

    response = await client.post(f"{config.OPENAPI_PREFIX}/applicants", json=data)
    assert response.status_code == status_code
    if expectation_response is not None:
        assert response.json() == expectation_response


@pytest.mark.parametrize(
    "data, status_code, expectation_response",
    [
        (
            GET_JOB_RECOMMENDATION_HAPPY_CASE["request"],
            status.HTTP_200_OK,
            GET_JOB_RECOMMENDATION_HAPPY_CASE["response"],
        ),
        (
            GET_JOB_RECOMMENDATION_HAPPY_CASE_WITH_WORKER_NOT_EXISTS["request"],
            status.HTTP_404_NOT_FOUND,
            GET_JOB_RECOMMENDATION_HAPPY_CASE_WITH_WORKER_NOT_EXISTS["response"],
        ),
    ],
)
async def test_api_get_job_recommandation_by_id(
    client, records, data, status_code, expectation_response
):
    await records(TEST_DATA_PATH)
    response = await client.get(
        f"{config.OPENAPI_PREFIX}/jobs/recommendations", query_string=data
    )
    assert response.status_code == status_code
    if expectation_response is not None:
        assert response.json() == expectation_response


@pytest.mark.parametrize(
    "worker_id, data, status_code, expectation_response",
    [
        (
            1,
            GET_SEARCH_JOB_HAPPY_CASE["request"],
            status.HTTP_200_OK,
            GET_SEARCH_JOB_HAPPY_CASE["response"],
        ),
        ("3fa85f64-5717-4562-b3fc-2c963f66afa6", None, status.HTTP_404_NOT_FOUND, None),
    ],
)
async def test_api_search_jobs(
    client, records, worker_id, data, status_code, expectation_response
):
    workers, jobs, applicants = await records(TEST_DATA_PATH)
    if isinstance(worker_id, int):
        worker_id = workers[worker_id - 1].uuid
    response = await client.get(
        f"{config.OPENAPI_PREFIX}/jobs/{worker_id}", query_string=data
    )
    assert response.status_code == status_code
    if expectation_response is not None:
        assert response.json() == expectation_response


@pytest.mark.parametrize(
    "worker_id, data, status_code",
    [
        (1, UPDATE_WORKER_HAPPY_CASE, status.HTTP_204_NO_CONTENT),
        (
            "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            UPDATE_WORKER_HAPPY_CASE,
            status.HTTP_404_NOT_FOUND,
        ),
    ],
)
async def test_api_update_worker(client, records, worker_id, status_code, data):
    workers, jobs, applicants = await records(TEST_DATA_PATH)
    if isinstance(worker_id, int):
        worker_id = workers[worker_id - 1].uuid

    response = await client.put(
        f"{config.OPENAPI_PREFIX}/workers/{worker_id}", json=data
    )
    assert response.status_code == status_code
