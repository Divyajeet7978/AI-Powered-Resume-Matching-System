from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional
import logging
from datetime import datetime
import os
from pathlib import Path
import uuid

from .database import database
from .nlp_processor import nlp_processor
from .tasks import process_resume_task

app = FastAPI(
    title="AI-Powered Resume Matching System",
    description="API for matching resumes with job descriptions using NLP",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class JobDescription(BaseModel):
    text: str

class ResumeMatchRequest(BaseModel):
    resume_id: str
    job_description: str

class ResumeUploadResponse(BaseModel):
    resume_id: str
    status: str
    message: str

@app.on_event("startup")
async def startup_db_client():
    try:
        # Test database connection
        database.db.command('ping')
        logger.info("Connected to the database!")
    except Exception as e:
        logger.error(f"Database connection error: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    database.close()
    logger.info("Database connection closed")

@app.post("/upload-resume/", response_model=ResumeUploadResponse)
async def upload_resume(file: UploadFile = File(...)):
    try:
        # Generate unique ID for the resume
        resume_id = str(uuid.uuid4())
        
        # Create uploads directory if not exists
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Save the file temporarily
        file_path = upload_dir / f"{resume_id}.pdf"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        
        # Store metadata in database
        resume_data = {
            "_id": resume_id,
            "original_filename": file.filename,
            "upload_date": datetime.utcnow(),
            "file_path": str(file_path),
            "status": "uploaded"
        }
        database.insert_resume(resume_data)
        
        return ResumeUploadResponse(
            resume_id=resume_id,
            status="success",
            message="Resume uploaded successfully"
        )
    except Exception as e:
        logger.error(f"Error uploading resume: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error uploading resume"
        )

@app.post("/match-resume/")
async def match_resume(request: ResumeMatchRequest):
    try:
        # Get resume from database
        resume = database.get_resume(request.resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        # Process the resume (async via Celery)
        task = process_resume_task.delay(request.resume_id, request.job_description)
        
        return JSONResponse(
            content={
                "status": "processing",
                "task_id": task.id,
                "resume_id": request.resume_id,
                "message": "Resume matching in progress"
            }
        )
    except Exception as e:
        logger.error(f"Error matching resume: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing resume"
        )

@app.get("/results/{resume_id}")
async def get_results(resume_id: str):
    try:
        resume = database.get_resume(resume_id)
        if not resume:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resume not found"
            )
        
        if "match_results" not in resume:
            return JSONResponse(
                content={
                    "status": "pending",
                    "message": "Results not ready yet"
                }
            )
        
        return JSONResponse(
            content={
                "status": "complete",
                "results": resume["match_results"]
            }
        )
    except Exception as e:
        logger.error(f"Error fetching results: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching results"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)