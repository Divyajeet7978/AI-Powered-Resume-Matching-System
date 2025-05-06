from celery import Celery
from nlp_processor import NLPProcessor
from database import Database
import config

app = Celery('tasks', broker=config.CELERY_BROKER_URL)
nlp = NLPProcessor()
db = Database(config.DATABASE_URL)

@app.task
def process_resume_task(job_id, resume_bytes):
    try:
        resume_text = extract_text_from_bytes(resume_bytes)
        job_desc = get_job_description(job_id)
        
        # Process with NLP
        skills = nlp.extract_skills(resume_text)
        score = nlp.calculate_similarity(resume_text, job_desc['text'])
        
        # Prepare and save results
        result = ResumeMatchResult(
            job_id=job_id,
            resume_id=generate_resume_id(),
            similarity_score=score,
            matched_skills=skills['matched'],
            missing_skills=skills['missing'],
            experience_match=calculate_experience_match(resume_text, job_desc)
        )
        
        db.save_results(result)
        return result.id
    except Exception as e:
        logger.error(f"Processing failed: {str(e)}")
        raise