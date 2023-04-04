CREATE_JOB_HAPPY_CASE = {
    "request": {
        "discipline": "LPN/LVN",
        "specialty": "ICU",
        "state": "CA",
        "pay_amount": 2500,
    },
    "response": None,
}

CREATE_JOB_MISSING_FIELDS = {
    "request": {"specialty": "ICU", "state": "CA", "pay_amount": 2500},
    "response": {
        "detail": [
            {
                "loc": ["body", "discipline"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    },
}

CREATE_JOB_INVALID_FIELDS = {
    "request": {
        "discipline": "LPN/LVN",
        "specialty": "1111",
        "state": "CA",
        "pay_amount": 2500,
    },
    "response": {
        "detail": [
            {
                "ctx": {"enum_values": ["ICU", "PCU", "DIALYSIS", "CVOR"]},
                "loc": ["body", "specialty"],
                "msg": "value is not a valid enumeration member; permitted: 'ICU', 'PCU', 'DIALYSIS', 'CVOR'",
                "type": "type_error.enum",
            }
        ]
    },
}

CREATE_WORKER_HAPPY_CASE = {
    "request": {
        "discipline": "RN",
        "specialties": ["ICU", "PCU"],
        "preferred_working_states": ["CA"],
        "avg_weekly_pay_amount": 2000,
    },
    "response": None,
}

CREATE_WORKER_MISSING_FIELDS = {
    "request": {
        "specialties": ["ICU", "PCU"],
        "preferred_working_states": ["CA"],
        "avg_weekly_pay_amount": 2000,
    },
    "response": {
        "detail": [
            {
                "loc": ["body", "discipline"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    },
}

CREATE_WORKER_INVALID_FIELDS = {
    "request": {
        "discipline": "123",
        "specialties": ["ICU", "PCU"],
        "preferred_working_states": ["CA"],
        "avg_weekly_pay_amount": 2000,
    },
    "response": {
        "detail": [
            {
                "ctx": {"enum_values": ["RN", "LPN/LVN", "PHYSICAL THERAPIST"]},
                "loc": ["body", "discipline"],
                "msg": "value is not a valid enumeration member; permitted: 'RN', 'LPN/LVN', 'PHYSICAL THERAPIST'",
                "type": "type_error.enum",
            }
        ]
    },
}

CREATE_APPLICANT_HAPPY_CASE = {
    "request": {"job_id": 1, "worker_id": 1},
    "response": None,
}

CREATE_APPLICANT_EXISTS = {
    "request": {"job_id": 3, "worker_id": 1},
    "response": {
        "message": "This applicant between worker 1 and job 3 is existed",
        "status": False,
    },
}


CREATE_WORKER_WITH_WORKER_NOT_EXISTS = {
    "request": {"job_id": 1, "worker_id": 4},
    "response": {"message": "Worker with id: 4 does not exist", "status": False},
}


GET_JOB_RECOMMENDATION_HAPPY_CASE = {
    "request": {"k_top": 10, "worker_id": 1},
    "response": {
        "message": None,
        "data": [
            {"job_id": "2", "matching_score": 100.0},
            {"job_id": "1", "matching_score": 50.0},
            {"job_id": "3", "matching_score": 25.0},
        ],
        "status": True,
    },
}


GET_JOB_RECOMMENDATION_HAPPY_CASE_WITH_WORKER_NOT_EXISTS = {
    "request": {"k_top": 10, "worker_id": 5},
    "response": {"message": "Worker with id: 5 does not exist", "status": False},
}


GET_SEARCH_JOB_HAPPY_CASE = {
    "request": {"discipline": "RN", "state": "CA", "wage_min": 1000},
    "response": {
        "message": None,
        "data": [{"job_id": "2", "matching_score": 100.0}],
        "status": True,
    },
}


UPDATE_WORKER_HAPPY_CASE = {"avg_weekly_pay_amount": 140.5}
