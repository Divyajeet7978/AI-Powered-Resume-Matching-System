import pytest
from nlp_processor import NLPProcessor

@pytest.fixture
def nlp_processor():
    return NLPProcessor()

def test_skill_extraction(nlp_processor):
    test_text = "Experienced in Python, JavaScript, and machine learning"
    skills = nlp_processor.extract_skills(test_text)
    assert "Python" in skills['matched']
    assert "JavaScript" in skills['matched']
    
def test_similarity_calculation(nlp_processor):
    resume = "Senior Python developer with 5 years experience"
    job_desc = "Looking for experienced Python developers"
    score = nlp_processor.calculate_similarity(resume, job_desc)
    assert 0 <= score <= 1