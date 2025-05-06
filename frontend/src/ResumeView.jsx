import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

const ResultsView = () => {
  const { taskId } = useParams();
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchResults = async () => {
      try {
        const response = await axios.get(`/api/results/${taskId}`);
        setResults(response.data);
      } catch (error) {
        console.error('Error fetching results:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [taskId]);

  if (loading) return <div>Loading results...</div>;
  if (!results) return <div>No results found</div>;

  const skillData = [
    { name: 'Matched Skills', value: results.matched_skills.length },
    { name: 'Missing Skills', value: results.missing_skills.length }
  ];

  return (
    <div className="results-container">
      <h2>Resume Matching Results</h2>
      <div className="score-section">
        <h3>Overall Match Score: {Math.round(results.similarity_score * 100)}%</h3>
      </div>
      
      <div className="chart-section">
        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={skillData}>
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="value" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="skills-section">
        <div className="matched-skills">
          <h4>Matched Skills ({results.matched_skills.length})</h4>
          <ul>
            {results.matched_skills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </div>
        
        <div className="missing-skills">
          <h4>Missing Skills ({results.missing_skills.length})</h4>
          <ul>
            {results.missing_skills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default ResultsView;