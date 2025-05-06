from sqlalchemy import create_engine, MetaData
from database import Base, ResumeMatchResult
import config

def initialize_database():
    engine = create_engine(config.DATABASE_URL)
    
    # Create all tables
    Base.metadata.create_all(engine)
    
    print("Database tables created successfully")

if __name__ == "__main__":
    initialize_database()