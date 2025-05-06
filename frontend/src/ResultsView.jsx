import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';

const ResultsContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 2rem;
`;

const ScoreCard = styled(motion.div)`
  background: white;
  border-radius: 15px;
  padding: 2rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  text-align: center;
  position: relative;
  overflow: hidden;

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 10px;
    background: linear-gradient(to right, #3498db, #2c3e50);
  }
`;

const ScoreCircle = styled.div`
  width: 150px;
  height: 150px;
  border-radius: 50%;
  background: ${props => {
    const score = props.score;
    if (score >= 80) return 'linear-gradient(135deg, #4CAF50, #8BC34A)';
    if (score >= 60) return 'linear-gradient(135deg, #FFC107, #FF9800)';
    return 'linear-gradient(135deg, #F44336, #E91E63)';
  }};
  margin: 0 auto 1rem;
  display: flex;
  justify-content: center;
  align-items: center;
  color: white;
  font-size: 2.5rem;
  font-weight: bold;
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
`;

const Section = styled(motion.div)`
  background: white;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
`;

const SectionTitle = styled.h3`
  color: #2c3e50;
  margin-top: 0;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 2px solid #f0f0f0;
`;

const SkillTag = styled.span`
  display: inline-block;
  background-color: #e0f7fa;
  color: #00838f;
  padding: 0.3rem 0.8rem;
  border-radius: 50px;
  margin: 0.3rem;
  font-size: 0.9rem;
`;

const RecommendationItem = styled(motion.li)`
  margin-bottom: 0.5rem;
  padding: 0.8rem;
  background-color: #f9f9f9;
  border-left: 4px solid #3498db;
  border-radius: 0 4px 4px 0;
`;

const ResetButton = styled(motion.button)`
  padding: 0.8rem 1.5rem;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-top: 1rem;
  align-self: flex-end;

  &:hover {
    background-color: #c0392b;
  }
`;

const ResultsView = ({ results, onReset }) => {
  return (
    <ResultsContainer>
      <ScoreCard
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
      >
        <h2>Your Resume Match Score</h2>
        <ScoreCircle score={results.match_score}>
          {Math.round(results.match_score)}%
        </ScoreCircle>
        <p>
          {results.match_score >= 80
            ? 'Excellent match! Your resume aligns very well with the job requirements.'
            : results.match_score >= 60
            ? 'Good match, but there are some areas for improvement.'
            : 'Needs improvement. Consider revising your resume to better match the job requirements.'}
        </p>
      </ScoreCard>

      <Section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        <SectionTitle>Skills Found</SectionTitle>
        <div>
          {results.extracted_entities.skills.map((skill, index) => (
            <SkillTag key={index}>{skill}</SkillTag>
          ))}
        </div>
      </Section>

      <Section
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <SectionTitle>Recommendations</SectionTitle>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {results.recommendations.map((rec, index) => (
            <RecommendationItem
              key={index}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 + index * 0.1 }}
            >
              {rec}
            </RecommendationItem>
          ))}
        </ul>
      </Section>

      <ResetButton
        onClick={onReset}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        Analyze Another Resume
      </ResetButton>
    </ResultsContainer>
  );
};

export default ResultsView;