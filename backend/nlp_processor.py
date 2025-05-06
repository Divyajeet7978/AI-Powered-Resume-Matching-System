import spacy
from transformers import BertForSequenceClassification, BertTokenizer
from skill_ontology import SkillOntology

class NLPProcessor:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_lg")
        self.tokenizer = BertTokenizer.from_pretrained('bert_model/')
        self.model = BertForSequenceClassification.from_pretrained('bert_model/')
        self.skill_ontology = SkillOntology('models/skill_ontology.json')

    def extract_skills(self, text):
        doc = self.nlp(text)
        return self.skill_ontology.match_skills([token.text for token in doc])

    def calculate_similarity(self, resume_text, job_desc_text):
        # Use fine-tuned BERT model to calculate semantic similarity
        inputs = self.tokenizer(resume_text, job_desc_text, return_tensors="pt")
        outputs = self.model(**inputs)
        return outputs.logits.item()