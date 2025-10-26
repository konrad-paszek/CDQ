import pytest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient
from cdq.analytics.api.app import app
from cdq.analytics.api.models.report_params import ReportParams


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_report_params():
    return {
        "report_id": "report_123",
        "title": "Test Report",
        "format": "xlsx",
        "job_id": None,
        "storage_id": "storage_001"
    }


@pytest.fixture
def sample_job_response():
    return {
        "status": "FINISHED",
        "context": {
            "workdir": "/tmp/test/storage_001",
            "content": [
                {
                    "path": "/tmp/test/storage_001/file1.xlsx",
                    "name": "file1.xlsx"
                },
                {
                    "path": "/tmp/test/storage_001/file2.xlsx",
                    "name": "file2.xlsx"
                }
            ]
        }
    }


class TestCreateReport:
    @patch('cdq.infra.airflow.trigger_reporting_job')
    def test_create_report_success(self, mock_trigger, client, sample_report_params):
        """Test poprawnego utworzenia raportu"""
        job_id = "job_abc123"
        mock_trigger.return_value = (201, {"job": {"id": job_id, "details": None}})
        
        response = client.post(
            "/reportingJob/report_123/create",
            json=sample_report_params
        )
        
        assert response.status_code == 200
        assert "job" in response.json()
        assert response.json()["job"]["id"] == job_id
        assert response.json()["job"]["details"] is None
        mock_trigger.assert_called_once()
    
    @patch('cdq.infra.airflow.trigger_reporting_job')
    def test_create_report_validates_params(self, mock_trigger, client):
        invalid_params = {
            "report_id": "report_123",
        }
        
        response = client.post(
            "/reportingJob/report_123/create",
            json=invalid_params
        )
        
        assert response.status_code == 422
        mock_trigger.assert_not_called()
    
    @patch('cdq.infra.airflow.trigger_reporting_job')
    def test_create_report_with_optional_job_id(self, mock_trigger, client, sample_report_params):
        sample_report_params["job_id"] = "custom_job_id"
        mock_trigger.return_value = (201, {"job": {"id": "custom_job_id", "details": None}})
        
        response = client.post(
            "/reportingJob/report_123/create",
            json=sample_report_params
        )
        
        assert response.status_code == 200
        called_params = mock_trigger.call_args[0][0]
        assert called_params["job_id"] == "custom_job_id"


class TestGetReportingJobStatus:
    @patch('cdq.infra.airflow.fetch_reporting_job')
    def test_get_job_status_success(self, mock_fetch, client, sample_job_response):
        job_id = "job_abc123"
        mock_fetch.return_value = (200, {"job": {"id": job_id, "details": sample_job_response}})
        
        response = client.get(f"/reportingJob/{job_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert "job" in data
        assert data["job"]["id"] == job_id
        assert data["job"]["details"]["status"] == "FINISHED"
        assert "context" in data["job"]["details"]
        assert "workdir" in data["job"]["details"]["context"]
        assert "content" in data["job"]["details"]["context"]
        mock_fetch.assert_called_once_with(job_id)
    
    @patch('cdq.infra.airflow.fetch_reporting_job')
    def test_get_job_status_not_found(self, mock_fetch, client):
        job_id = "nonexistent_job"
        mock_fetch.return_value = (400, f"Job `{job_id}` not found")
        
        response = client.get(f"/reportingJob/{job_id}")
        
        assert response.status_code == 200
        assert "not found" in response.json().lower()
        mock_fetch.assert_called_once_with(job_id)
    
    @patch('cdq.infra.airflow.fetch_reporting_job')
    def test_get_job_status_running(self, mock_fetch, client):
        job_id = "running_job"
        running_response = {
            "status": "RUNNING",
            "context": {
                "workdir": "/tmp/test/storage_001",
                "content": []
            }
        }
        mock_fetch.return_value = (200, {"job": {"id": job_id, "details": running_response}})
        
        response = client.get(f"/reportingJob/{job_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["job"]["details"]["status"] == "RUNNING"


class TestListReportingJobs:
    @patch('cdq.infra.airflow.list_jobs')
    def test_list_jobs_empty(self, mock_list, client):
        mock_list.return_value = (200, {"jobs": {}})
        
        response = client.get("/reportingJobs")
        
        assert response.status_code == 200
        data = response.json()
        assert "jobs" in data
        assert len(data["jobs"]) == 0
        mock_list.assert_called_once()
    
    @patch('cdq.infra.airflow.list_jobs')
    def test_list_jobs_multiple(self, mock_list, client, sample_job_response):
        jobs_dict = {
            "job_1": sample_job_response,
            "job_2": {
                "status": "RUNNING",
                "context": {
                    "workdir": "/tmp/test/storage_002",
                    "content": []
                }
            },
            "job_3": {
                "status": "ERROR",
                "context": {
                    "workdir": "/tmp/test/storage_003",
                    "content": []
                }
            }
        }
        mock_list.return_value = (200, {"jobs": jobs_dict})
        
        response = client.get("/reportingJobs")
        
        assert response.status_code == 200
        data = response.json()
        assert "jobs" in data
        assert len(data["jobs"]) == 3
        assert "job_1" in data["jobs"]
        assert "job_2" in data["jobs"]
        assert "job_3" in data["jobs"]
        assert data["jobs"]["job_1"]["status"] == "FINISHED"
        assert data["jobs"]["job_2"]["status"] == "RUNNING"
        assert data["jobs"]["job_3"]["status"] == "ERROR"
        mock_list.assert_called_once()
    
    @patch('cdq.infra.airflow.list_jobs')
    def test_list_jobs_with_content(self, mock_list, client):
        jobs_with_files = {
            "job_with_files": {
                "status": "FINISHED",
                "context": {
                    "workdir": "/tmp/test/storage_001",
                    "content": [
                        {"path": "/tmp/test/file1.xlsx", "name": "file1.xlsx"},
                        {"path": "/tmp/test/file2.xlsx", "name": "file2.xlsx"}
                    ]
                }
            }
        }
        mock_list.return_value = (200, {"jobs": jobs_with_files})
        
        response = client.get("/reportingJobs")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["jobs"]["job_with_files"]["context"]["content"]) == 2
        assert all("path" in item for item in data["jobs"]["job_with_files"]["context"]["content"])
        assert all("name" in item for item in data["jobs"]["job_with_files"]["context"]["content"])