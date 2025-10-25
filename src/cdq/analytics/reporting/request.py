from dataclasses import dataclass, field
from typing import Optional
from uuid import uuid4

from cdq.analytics.resources import ResourceInfo, ResourceLookup


@dataclass
class ReportRequest:
    info: ResourceInfo
    title: str
    format: str
    storage_id: str
    job_id: Optional[str] = None

    @property
    def context_path(self):
        if not self.job_id:
            self.job_id = uuid4().hex
        return f"{self.storage_id}/{self.job_id}"


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
    return ReportRequest(info, title, format, storage_id)
