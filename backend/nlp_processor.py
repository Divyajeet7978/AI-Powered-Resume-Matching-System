import spacy
from transformers import BertTokenizer, BertModel
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import json
import logging
from typing import Dict, Tuple, List
import yaml
from pathlib import Path

class NLPProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.nlp = None
        self.bert_tokenizer = None
        self.bert_model = None
        self.skill_ontology = None
        self._load_models()
        self._load_config()
    
    def _load_models(self):
        try:
            # Load spaCy model
            self.nlp = spacy.load("en_core_web_lg")
            
            # Load BERT model
            model_path = Path(__file__).parent.parent / "models" / "bert_model"
            if model_path.exists():
                self.bert_tokenizer = BertTokenizer.from_pretrained(str(model_path))
                self.bert_model = BertModel.from_pretrained(str(model_path))
            else:
                self.bert_tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
                self.bert_model = BertModel.from_pretrained('bert-base-uncased')
            
            # Load skill ontology
            ontology_path = Path(__file__).parent.parent / "models" / "skill_ontology.json"
            with open(ontology_path, 'r') as f:
                self.skill_ontology = json.load(f)
            
            self.logger.info("All NLP models loaded successfully")
        except Exception as e:
            self.logger.error(f"Error loading models: {e}")
            raise
    
    def _load_config(self):
        try:
            config_path = Path(__file__).parent.parent / "config" / "nlp_config.yaml"
            with open(config_path, 'r') as f:
                self.config = yaml.safe_load(f)
        except Exception as e:
            self.logger.error(f"Error loading NLP config: {e}")
            raise
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        doc = self.nlp(text)
        entities = {
            "skills": [],
            "experience": [],
            "education": [],
            "certifications": []
        }
        
        # Extract skills using both NER and ontology matching
        for token in doc:
            if token.text.lower() in self.skill_ontology:
                entities["skills"].append(token.text)
        
        # Extract experience (simple pattern matching for demo)
        for ent in doc.ents:
            if ent.label_ == "DATE":
                entities["experience"].append(ent.text)
        
        return entities
    
    def get_bert_embedding(self, text: str) -> np.ndarray:
        inputs = self.bert_tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.bert_model(**inputs)
        return outputs.last_hidden_state.mean(dim=1).squeeze().numpy()
    
    def calculate_similarity(self, resume_text: str, job_desc_text: str) -> float:
        resume_embedding = self.get_bert_embedding(resume_text)
        job_embedding = self.get_bert_embedding(job_desc_text)
        similarity = cosine_similarity([resume_embedding], [job_embedding])[0][0]
        return float(similarity * 100)  # Convert to percentage
    
    def process_resume(self, resume_text: str, job_description: str) -> Dict[str, any]:
        entities = self.extract_entities(resume_text)
        similarity_score = self.calculate_similarity(resume_text, job_description)
        
        return {
            "extracted_entities": entities,
            "match_score": similarity_score,
            "recommendations": self._generate_recommendations(entities, job_description)
        }
    
    def _generate_recommendations(self, entities: Dict[str, List[str]], job_desc: str) -> List[str]:
        doc = self.nlp(job_desc)
        job_skills = set()
        
        for token in doc:
            if token.text.lower() in self.skill_ontology:
                job_skills.add(token.text.lower())
        
        resume_skills = set(skill.lower() for skill in entities["skills"])
        missing_skills = job_skills - resume_skills
        
        recommendations = []
        if missing_skills:
            recommendations.append(f"Consider adding these skills: {', '.join(missing_skills)}")
        
        return recommendations

# Singleton instance
nlp_processor = NLPProcessor()