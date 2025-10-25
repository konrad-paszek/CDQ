import threading
import time
from queue import Queue

from cdq.analytics.reporting.job import REPORTING_JOB_PARAMS, ReportingJob

xcom = {}
lock = threading.RLock()


def run_job(job):
    # job = ReportingJob(params)
    resp = job.execute()
    with lock:
        xcom.update({job.jobid: resp.to_dict()})


def trigger_reporting_job(params):
    job = ReportingJob(params)
    t = threading.Thread(target=run_job, args=(job,))
    t.start()
    return 201, {"job": {"id": job.jobid, "details": None}}


def fetch_reporting_job(job_id):
    if job_id not in xcom:
        return 400, f"Job `{job_id}` not found"
    return 200, {"job": {"id": job_id, "details": xcom.get(job_id)}}


def list_jobs():
    return 200, {"jobs": xcom}
