from fastapi import FastAPI

from cdq.analytics.api.models.report_params import ReportParams
import cdq.infra.airflow as backend

app = FastAPI()

# NOTE: What, no pydantic?

@app.post("/reportingJob/{reportId}/create")
def create_report(params: ReportParams):
    status, details = backend.trigger_reporting_job(params.model_dump())
    return details


@app.get("/reportingJob/{job_id}")
def get_reporting_job_status(job_id: str):
    status, details = backend.fetch_reporting_job(job_id)
    return details


@app.get("/reportingJobs")
def list_reporting_jobs():
    status, details = backend.list_jobs()
    return details
