// ResumeUploader.jsx
import React, { useState } from 'react';
import axios from 'axios';

function ResumeUploader() {
  const [file, setFile] = useState(null);
  const [jobDesc, setJobDesc] = useState('');
  const [results, setResults] = useState([]);
  
  const handleUpload = async () => {
    const formData = new FormData();
    formData.append('file', file);
    
    const response = await axios.post('/upload-resume/', formData);
    const resumeId = response.data.resume_id;
    
    const matchResponse = await axios.post('/match-resumes/', {
      text: jobDesc,
      required_skills: extractSkills(jobDesc) // Implement skill extraction
    });
    
    setResults(matchResponse.data);
  };

  return (
    <div>
      <input type="file" onChange={e => setFile(e.target.files[0])} />
      <textarea 
        placeholder="Paste job description"
        value={jobDesc}
        onChange={e => setJobDesc(e.target.value)}
      />
      <button onClick={handleUpload}>Match Resumes</button>
      
      <div className="results">
        {results.map((resume, idx) => (
          <div key={idx} className="resume-card">
            <h3>Score: {resume.score.toFixed(2)}</h3>
            <p>Skills: {resume.skills.join(', ')}</p>
            <p>Experience: {resume.experience} years</p>
          </div>
        ))}
      </div>
    </div>
  );
}