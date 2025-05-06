import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axios from 'axios';

import ResumeUploader from './ResumeUploader';
import ResultsView from './ResultsView';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 2rem;
`;

const Header = styled(motion.header)`
  text-align: center;
  margin-bottom: 3rem;
  h1 {
    font-size: 2.5rem;
    color: #2c3e50;
    margin-bottom: 0.5rem;
    background: linear-gradient(to right, #3498db, #2c3e50);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  p {
    font-size: 1.2rem;
    color: #7f8c8d;
  }
`;

const MainContent = styled(motion.div)`
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  padding: 2rem;
  overflow: hidden;
`;

function App() {
  const [resumeId, setResumeId] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [results, setResults] = useState(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [taskId, setTaskId] = useState(null);

  const handleUploadSuccess = (id) => {
    setResumeId(id);
    toast.success('Resume uploaded successfully!');
  };

  const handleMatchResume = async () => {
    if (!resumeId || !jobDescription.trim()) {
      toast.error('Please upload a resume and enter a job description');
      return;
    }

    try {
      setIsProcessing(true);
      const response = await axios.post('http://localhost:8000/match-resume/', {
        resume_id: resumeId,
        job_description: jobDescription
      });

      setTaskId(response.data.task_id);
      pollForResults(resumeId);
    } catch (error) {
      console.error('Error matching resume:', error);
      toast.error('Failed to process resume');
      setIsProcessing(false);
    }
  };

  const pollForResults = async (resumeId) => {
    try {
      const response = await axios.get(`http://localhost:8000/results/${resumeId}`);
      if (response.data.status === 'complete') {
        setResults(response.data.results);
        setIsProcessing(false);
        toast.success('Resume analysis complete!');
      } else {
        setTimeout(() => pollForResults(resumeId), 2000);
      }
    } catch (error) {
      console.error('Error polling for results:', error);
      setIsProcessing(false);
    }
  };

  return (
    <AppContainer>
      <Header
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <h1>AI-Powered Resume Matcher</h1>
        <p>Upload your resume and get instant feedback on job fit</p>
      </Header>

      <MainContent
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        {!results ? (
          <ResumeUploader
            resumeId={resumeId}
            jobDescription={jobDescription}
            setJobDescription={setJobDescription}
            onUploadSuccess={handleUploadSuccess}
            onMatchResume={handleMatchResume}
            isProcessing={isProcessing}
          />
        ) : (
          <ResultsView 
            results={results}
            onReset={() => {
              setResults(null);
              setResumeId(null);
              setJobDescription('');
            }}
          />
        )}
      </MainContent>

      <ToastContainer 
        position="top-right"
        autoClose={5000}
        hideProgressBar={false}
        newestOnTop={false}
        closeOnClick
        rtl={false}
        pauseOnFocusLoss
        draggable
        pauseOnHover
      />
    </AppContainer>
  );
}

export default App;