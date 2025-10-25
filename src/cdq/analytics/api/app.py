from fastapi import FastAPI

import cdq.infra.airflow as backend

app = FastAPI()

# NOTE: What, no pydantic?


@app.post("/reportingJob/{reportId}/create")
def create_report(params: dict):
    raise NotImplementedError


@app.get("/reportingJob/{id}")
def get_reporting_job_status(job_id: str):
    status, details = backend.fetch_reporting_job(job_id)
    return details


@app.get("reportingJobs")
def list_reporting_jobs():
    status, details = backend.list_jobs()
    return details
