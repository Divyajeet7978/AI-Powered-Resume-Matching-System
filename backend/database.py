# database.py
import pinecone
import os

class ResumeDatabase:
    def __init__(self):
        pinecone.init(api_key=os.getenv("PINECONE_API_KEY"),
                    environment="us-west1-gcp")
        
        self.index_name = "resume-matcher"
        if self.index_name not in pinecone.list_indexes():
            pinecone.create_index(
                name=self.index_name,
                dimension=384,  # matches MiniLM embedding size
                metric="cosine"
            )
        
        self.index = pinecone.Index(self.index_name)
        self.metadata_store = {}  # In production, use MongoDB/PostgreSQL

    def store_resume(self, resume_id, text, entities, embedding):
        self.index.upsert([
            (resume_id, embedding.tolist(), {
                'text': text,
                'skills': entities['skills'],
                'experience': entities['experience']
            })
        ])
        self.metadata_store[resume_id] = entities

    def get_all_resumes(self):
        # In production, implement pagination
        return [
            {'resume_id': id, 'embedding': self.index.fetch([id])['vectors'][id]['values'],
            'entities': self.metadata_store[id]
            for id in self.metadata_store
        ]