from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

from src.cdq.analytics.cli.report_generate import app, report_mapping

runner = CliRunner()

def test_report_mapping_known():
    assert report_mapping("DUMP_REPORT") == "business_partner_report"

def test_report_mapping_unknown():
    assert report_mapping("UNKNOWN_REPORT") == ""

@patch("src.cdq.analytics.cli.report_generate.ReportingJob")
def test_report_generate_command(mock_job_class):
    mock_job = MagicMock()
    mock_job.execute.return_value.to_dict.return_value = {"status": "success"}
    mock_job_class.return_value = mock_job

    result = runner.invoke(
        app,
        ["analytics", "report-generate", "DUMP_REPORT", "--title", "Test Title", "--format", "xlsx"],
    )
    assert result.exit_code == 0
    assert "Report generation status: success" in result.output

    mock_job_class.assert_called_once()
    mock_job_class.assert_called_with({
        "report_id": "business_partner_report",
        "title": "Test Title",
        "format": "xlsx",
        "storage_id": "storage_one",
    })
    mock_job.execute.assert_called_once()

@patch("src.cdq.analytics.cli.report_generate.ReportingJob")
def test_report_generate_command_no_format(mock_job_class):
    mock_job = MagicMock()
    mock_job.execute.return_value.to_dict.return_value = {"status": "done"}
    mock_job_class.return_value = mock_job
    
    result = runner.invoke(
        app,
        ["analytics", "report-generate", "DUMP_REPORT", "--title", "Default Format Test"],
    )
    assert result.exit_code == 0
    assert "Report generation status: done" in result.output

    mock_job_class.assert_called_once()
    mock_job_class.assert_called_with({
        "report_id": "business_partner_report",
        "title": "Default Format Test",
        "format": "xlsx",
        "storage_id": "storage_one",
    })
    mock_job.execute.assert_called_once()
