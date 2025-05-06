from pymongo import MongoClient
import logging
from pathlib import Path
import yaml

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_database():
    try:
        # Load configuration
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Connect to MongoDB
        client = MongoClient(config['database']['mongodb_uri'])
        db = client[config['database']['database_name']]
        
        # Create indexes
        db.resumes.create_index("upload_date")
        db.resumes.create_index("status")
        
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        raise

if __name__ == "__main__":
    initialize_database()