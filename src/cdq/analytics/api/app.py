from fastapi import FastAPI, Response

import cdq.infra.airflow as backend
from cdq.analytics.api.models.report_params import ReportParams

app = FastAPI()


@app.post("/reportingJob/{reportId}/create")
def create_report(reportId: str, params: ReportParams, response: Response):
    status, details = backend.trigger_reporting_job(reportId, params.model_dump())
    response.status_code = status
    return details


@app.get("/reportingJob/{job_id}")
def get_reporting_job_status(job_id: str, response: Response):
    status, details = backend.fetch_reporting_job(job_id)
    response.status_code = status
    return details


@app.get("/reportingJobs")
def list_reporting_jobs(response: Response):
    status, details = backend.list_jobs()
    response.status_code = status
    return details
