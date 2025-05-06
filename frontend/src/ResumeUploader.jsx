import React, { useState } from 'react';
import axios from 'axios';

const ResumeUploader = ({ onUpload }) => {
  const [jobId, setJobId] = useState('');
  const [file, setFile] = useState(null);
  
  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('resume', file);
    formData.append('job_id', jobId);
    
    try {
      const response = await axios.post('/api/upload-resume/', formData);
      onUpload(response.data.task_id);
    } catch (error) {
      console.error('Upload failed:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={jobId} onChange={(e) => setJobId(e.target.value)} placeholder="Job ID" />
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button type="submit">Upload and Match</button>
    </form>
  );
};