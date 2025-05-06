# main.py
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import nlp_processor
import database
import uuid
import asyncio

app = FastAPI()
nlp = nlp_processor.NLPProcessor()
db = database.ResumeDatabase()

class JobDescription(BaseModel):
    text: str
    required_skills: List[str]
    min_experience: int = 0

@app.post("/upload-resume/")
async def upload_resume(file: UploadFile = File(...)):
    file_content = await file.read()
    text = parse_file(file_content, file.filename)
    
    resume_id = str(uuid.uuid4())
    entities = nlp.extract_entities(text)
    embedding = nlp.get_embeddings(text)
    
    db.store_resume(
        resume_id=resume_id,
        text=text,
        entities=entities,
        embedding=embedding
    )
    
    return {"resume_id": resume_id}

@app.post("/match-resumes/")
async def match_resumes(job: JobDescription):
    job_embedding = nlp.get_embeddings(job.text)
    resumes = db.get_all_resumes()
    
    results = []
    for resume in resumes:
        similarity = nlp.calculate_similarity(
            resume['embedding'],
            job_embedding
        )
        
        # Add skill matching logic
        skill_match = len(set(resume['entities']['skills']) & 
                         set(job.required_skills)) / len(job.required_skills)
        
        score = 0.6*similarity + 0.4*skill_match
        
        results.append({
            'resume_id': resume['resume_id'],
            'score': score,
            'skills': resume['entities']['skills'],
            'experience': resume['entities']['experience']
        })
    
    return sorted(results, key=lambda x: x['score'], reverse=True)[:10]