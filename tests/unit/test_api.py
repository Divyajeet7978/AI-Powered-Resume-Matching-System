import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_upload_resume():
    test_file = ("resume.pdf", open("tests/sample_resume.pdf", "rb"), "application/pdf")
    response = client.post(
        "/api/upload-resume/",
        files={"resume": test_file},
        data={"job_id": "test_job_123"}
    )
    assert response.status_code == 200
    assert "task_id" in response.json()

def test_get_results():
    # First create a test task
    test_file = ("resume.pdf", open("tests/sample_resume.pdf", "rb"), "application/pdf")
    upload_response = client.post(
        "/api/upload-resume/",
        files={"resume": test_file},
        data={"job_id": "test_job_123"}
    )
    task_id = upload_response.json()["task_id"]
    
    # Then test results endpoint
    response = client.get(f"/api/results/{task_id}")
    assert response.status_code == 200
    assert "similarity_score" in response.json()