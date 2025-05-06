from sqlalchemy import create_engine, Column, String, JSON, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ResumeMatchResult(Base):
    __tablename__ = 'resume_matches'
    
    id = Column(String, primary_key=True)
    job_id = Column(String)
    resume_id = Column(String)
    similarity_score = Column(Float)
    matched_skills = Column(JSON)
    missing_skills = Column(JSON)
    experience_match = Column(Float)
    
class Database:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)
        
    def save_results(self, results):
        session = self.Session()
        session.add(results)
        session.commit()
        session.close()