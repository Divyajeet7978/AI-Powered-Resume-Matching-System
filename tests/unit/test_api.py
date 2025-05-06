import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os

from backend.main import app
from backend.database import database

client = TestClient(app)

@pytest.fixture(autouse=True)
def mock_env_vars(monkeypatch):
    monkeypatch.setenv("MONGODB_URI", "mongodb://test:test@localhost:27017")

@pytest.fixture
def mock_db():
    with patch('backend.database.MongoClient') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        mock_db_instance = MagicMock()
        mock_instance.__getitem__.return_value = mock_db_instance
        mock_collection = MagicMock()
        mock_db_instance.__getitem__.return_value = mock_collection
        yield mock_collection

def test_upload_resume(mock_db):
    mock_db.insert_one.return_value.inserted_id = "test123"
    
    test_file = ("test.pdf", open("tests/test.pdf", "rb"), "application/pdf")
    
    response = client.post(
        "/upload-resume/",
        files={"file": test_file}
    )
    
    assert response.status_code == 200
    assert response.json()["resume_id"] == "test123"
    assert response.json()["status"] == "success"

def test_match_resume(mock_db):
    mock_db.find_one.return_value = {"_id": "test123", "status": "uploaded"}
    
    response = client.post(
        "/match-resume/",
        json={
            "resume_id": "test123",
            "job_description": "test job description"
        }
    )
    
    assert response.status_code == 200
    assert response.json()["status"] == "processing"
    assert "task_id" in response.json()

def test_get_results_not_found(mock_db):
    mock_db.find_one.return_value = None
    
    response = client.get("/results/nonexistent")
    
    assert response.status_code == 404
    assert response.json()["detail"] == "Resume not found"

def test_get_results_pending(mock_db):
    mock_db.find_one.return_value = {"_id": "test123", "status": "uploaded"}
    
    response = client.get("/results/test123")
    
    assert response.status_code == 200
    assert response.json()["status"] == "pending"