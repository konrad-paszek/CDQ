import os
from typing import Optional

import typer

from cdq.analytics.reporting.job import ReportingJob

app = typer.Typer()
analytics = typer.Typer()


@analytics.command()
def report_generate(
    report_id: str,
    title: str = typer.Option(..., help="Report title"),
    format: Optional[str] = typer.Option(
        "xlsx", "--format", "-f", help="Report format"
    ),
):
    os.environ["CDQ__CORE__NODE"] = ".env"
    params = {
        "report_id": report_mapping(report_id),
        "title": title,
        "format": format,
        "storage_id": "storage_one",
    }
    print(report_id)
    job = ReportingJob(params)
    result = job.execute()
    typer.echo(f"Report generation status: {result.to_dict()['status']}")


app.add_typer(analytics, name="analytics")


def report_mapping(report_id: str) -> str:
    mapping = {"DUMP_REPORT": "business_partner_report"}
    return mapping.get(report_id, "")


if __name__ == "__main__":
    app()
