import spacy
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NLPProcessor:
    def __init__(self):
        logger.info("Loading NLP models...")
        self.nlp = spacy.load("en_core_web_lg")
        self.bert_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.tfidf = TfidfVectorizer(stop_words='english')
        logger.info("NLP models loaded successfully")
        
    def extract_entities(self, text):
        try:
            doc = self.nlp(text)
            return {
                'skills': list(set(ent.text for ent in doc.ents if ent.label_ == "SKILL")),
                'experience': self._extract_experience(doc),
                'education': list(set(ent.text for ent in doc.ents if ent.label_ == "EDU"))
            }
        except Exception as e:
            logger.error(f"Entity extraction failed: {str(e)}")
            raise

    def _extract_experience(self, doc):
        # Implement your experience extraction logic
        return 0  # Placeholder
        
    def get_embeddings(self, text):
        return self.bert_model.encode(text)
    
    def calculate_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2)/(np.linalg.norm(vec1)*np.linalg.norm(vec2))