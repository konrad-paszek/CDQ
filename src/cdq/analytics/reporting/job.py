from uuid import uuid4

from .main import client, request

REPORTING_JOB_PARAMS = {
    "report_id": None,
    "title": None,
    "format": None,
    "job_id": None,
}


class ReportingJob:
    def __init__(self, params: dict):
        self.params = params
        self.jobid = uuid4().hex
        self.params.update({"job_id": self.jobid})

    def execute(self):
        job_client = client()
        req = request(**self.params)
        return job_client.submit(req)
