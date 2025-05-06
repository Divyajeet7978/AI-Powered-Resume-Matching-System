from celery import Celery
import logging
from pathlib import Path
import PyPDF2
import time

from .database import database
from .nlp_processor import nlp_processor

# Configure Celery
app = Celery(
    'resume_matcher',
    broker='redis://localhost:6379/0',
    backend='redis://localhost:6379/1'
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.task(bind=True)
def process_resume_task(self, resume_id: str, job_description: str):
    try:
        # Update task status
        self.update_state(state='PROGRESS', meta={'progress': 10})
        
        # Get resume from database
        resume = database.get_resume(resume_id)
        if not resume:
            raise ValueError(f"Resume {resume_id} not found")
        
        # Extract text from PDF
        file_path = Path(resume["file_path"])
        if not file_path.exists():
            raise ValueError(f"File not found at {file_path}")
        
        self.update_state(state='PROGRESS', meta={'progress': 30})
        
        text = ""
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        
        self.update_state(state='PROGRESS', meta={'progress': 60})
        
        # Process the resume text
        results = nlp_processor.process_resume(text, job_description)
        
        self.update_state(state='PROGRESS', meta={'progress': 80})
        
        # Save results to database
        database.update_match_results(resume_id, results)
        
        return {
            'status': 'SUCCESS',
            'result': {
                'resume_id': resume_id,
                'match_score': results['match_score']
            }
        }
    except Exception as e:
        logger.error(f"Error processing resume {resume_id}: {e}")
        raise self.retry(exc=e, countdown=60)