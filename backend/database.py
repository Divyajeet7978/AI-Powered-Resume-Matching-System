from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from typing import Optional, Dict, Any
import logging
from dotenv import load_dotenv
import os

load_dotenv()

class Database:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.logger = logging.getLogger(__name__)
        self.client = None
        self.db = None
        self._connect()
    
    def _connect(self):
        try:
            mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
            self.client = MongoClient(mongodb_uri, serverSelectionTimeoutMS=5000)
            self.db = self.client["resume_matcher"]
            # Test the connection
            self.client.admin.command('ismaster')
            self.logger.info("Successfully connected to MongoDB")
        except ConnectionFailure as e:
            self.logger.error(f"Failed to connect to MongoDB: {e}")
            raise
    
    def insert_resume(self, resume_data: Dict[str, Any]) -> str:
        try:
            result = self.db.resumes.insert_one(resume_data)
            return str(result.inserted_id)
        except Exception as e:
            self.logger.error(f"Error inserting resume: {e}")
            raise
    
    def get_resume(self, resume_id: str) -> Optional[Dict[str, Any]]:
        try:
            return self.db.resumes.find_one({"_id": resume_id})
        except Exception as e:
            self.logger.error(f"Error fetching resume {resume_id}: {e}")
            return None
    
    def update_match_results(self, resume_id: str, match_data: Dict[str, Any]) -> bool:
        try:
            result = self.db.resumes.update_one(
                {"_id": resume_id},
                {"$set": {"match_results": match_data}}
            )
            return result.modified_count > 0
        except Exception as e:
            self.logger.error(f"Error updating match results for {resume_id}: {e}")
            return False
    
    def close(self):
        if self.client:
            self.client.close()
            self.logger.info("MongoDB connection closed")

# Singleton instance
database = Database()