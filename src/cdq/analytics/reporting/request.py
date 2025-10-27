from typing import Optional
from pydantic import BaseModel
from uuid import uuid4

from cdq.analytics.resources import ResourceLookup
from cdq.analytics.resources.reports import ReportInfo


class ReportRequest(BaseModel):
    info: ReportInfo
    title: str
    format: str
    storage_id: str
    job_id: Optional[str] = None

    @property
    def context_path(self) -> str:
        job_id = self.job_id or uuid4().hex
        object.__setattr__(self, 'job_id', job_id)
        return f"{self.storage_id}/{job_id}"


def request(**kwargs):
    report_id = kwargs.get("report_id")
    if not report_id:
        raise ValueError("no `report_id` provided")
    info = ResourceLookup.getinfo(report_id)
    if not info:
        raise ValueError("invaid `report_id` provided")
    title = kwargs.get("title", "Report")
    format = kwargs.get("format", "xlsx")
    storage_id = kwargs.get("storage_id")
    if not storage_id:
        raise ValueError("`storage_id` not provided")
    return ReportRequest(info=info, title=title, format=format, storage_id=storage_id, job_id=kwargs.get("job_id"))
