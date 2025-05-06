# nlp_processor.py
import spacy
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.bert_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf = TfidfVectorizer(stop_words='english')
        
    def extract_entities(self, text):
        doc = self.nlp(text)
        return {
            'skills': [ent.text for ent in doc.ents if ent.label_ == "SKILL"],
            'experience': self._extract_experience(doc),
            'education': [ent.text for ent in doc.ents if ent.label_ == "EDU"]
        }
    
    def _extract_experience(self, doc):
        # Implement date parsing and role duration calculation
        pass
    
    def get_embeddings(self, text):
        return self.bert_model.encode(text)
    
    def calculate_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))