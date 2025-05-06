from fastapi import FastAPI, UploadFile, HTTPException
from nlp_processor import process_resume
from database import save_results
from models import ResumeMatchResult
from celery_worker import process_resume_task

app = FastAPI()

@app.post("/api/upload-resume/")
async def upload_resume(job_id: str, resume: UploadFile):
    try:
        # Async processing via Celery
        task = process_resume_task.delay(job_id, await resume.read())
        return {"task_id": task.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/results/{task_id}")
async def get_results(task_id: str):
    # Check task status and return results when ready
    ...