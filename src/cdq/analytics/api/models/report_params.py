from pydantic import BaseModel

class ReportParams(BaseModel):
    report_id: str
    title: str
    format: str
    job_id: str | None = None
    storage_id: str
