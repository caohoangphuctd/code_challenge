import json
from pathlib import Path
from typing import Dict, List, Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from app import controllers, schemas
from app.database.models import Applicants, Jobs, Workers

PATH_DATA_ROOT = Path(__file__).parent / "data"


def load_data(path: str) -> Dict:
    with open(PATH_DATA_ROOT / path) as f:
        return json.load(f)


async def create_records(
    session: AsyncSession, path: str
) -> Tuple[List[Workers], List[Jobs], List[Applicants]]:
    workers = []
    jobs = []
    applicants = []

    data = load_data(path)
    for worker in data["worker"]:
        worker_record = await controllers.worker.create_worker(
            session, schemas.worker.CreateWorkerRequest.parse_obj(worker)
        )
        workers.append(worker_record)

    for job in data["job"]:
        job_record = await controllers.job.create_job(
            session, schemas.job.CreateJobRequest.parse_obj(job)
        )
        jobs.append(job_record)

    for applicant in data["applicant"]:
        applicant_record = await controllers.users.create_applicant(
            session, schemas.users.CreateApplicantRequest.parse_obj(applicant)
        )
        applicants.append(applicant_record)

    return workers, jobs, applicants  # type: ignore
