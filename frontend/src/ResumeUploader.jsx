import React, { useCallback, useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import axios from 'axios';

const UploadContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2rem;
`;

const UploadBox = styled(motion.div)`
  width: 100%;
  max-width: 600px;
  height: 300px;
  border: 3px dashed #3498db;
  border-radius: 15px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background-color: ${props => props.isDragging ? '#f0f8ff' : 'white'};
  
  &:hover {
    border-color: #2980b9;
    background-color: #f0f8ff;
  }

  svg {
    width: 80px;
    height: 80px;
    margin-bottom: 1rem;
    fill: #3498db;
  }

  p {
    color: #7f8c8d;
    text-align: center;
    margin: 0.5rem 0;
  }

  .file-name {
    font-weight: bold;
    color: #2c3e50;
    margin-top: 1rem;
  }
`;

const JobDescriptionInput = styled.textarea`
  width: 100%;
  max-width: 600px;
  min-height: 150px;
  padding: 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  resize: vertical;
  transition: all 0.3s ease;

  &:focus {
    outline: none;
    border-color: #3498db;
    box-shadow: 0 0 0 2px rgba(52, 152, 219, 0.2);
  }
`;

const MatchButton = styled(motion.button)`
  padding: 1rem 2rem;
  background: linear-gradient(to right, #3498db, #2c3e50);
  color: white;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: bold;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: 0 4px 15px rgba(52, 152, 219, 0.3);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(52, 152, 219, 0.4);
  }

  &:disabled {
    background: #bdc3c7;
    cursor: not-allowed;
    transform: none;
    box-shadow: none;
  }
`;

const LoadingSpinner = styled.div`
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;

  @keyframes spin {
    to { transform: rotate(360deg); }
  }
`;

const ResumeUploader = ({ 
  resumeId, 
  jobDescription, 
  setJobDescription, 
  onUploadSuccess, 
  onMatchResume, 
  isProcessing 
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [fileName, setFileName] = useState('');
  const [isUploading, setIsUploading] = useState(false);

  const handleDragEnter = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDragOver = (e) => {
    e.preventDefault();
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFile(e.target.files[0]);
    }
  };

  const handleFile = async (file) => {
    if (file.type !== 'application/pdf') {
      alert('Please upload a PDF file');
      return;
    }

    setFileName(file.name);
    setIsUploading(true);

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post(
        'http://localhost:8000/upload-resume/',
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        }
      );

      onUploadSuccess(response.data.resume_id);
    } catch (error) {
      console.error('Error uploading file:', error);
      alert('Failed to upload resume');
    } finally {
      setIsUploading(false);
    }
  };

  const triggerFileInput = useCallback(() => {
    document.getElementById('file-input').click();
  }, []);

  return (
    <UploadContainer>
      <input
        id="file-input"
        type="file"
        accept=".pdf"
        onChange={handleFileChange}
        style={{ display: 'none' }}
      />

      <UploadBox
        isDragging={isDragging}
        onClick={triggerFileInput}
        onDragEnter={handleDragEnter}
        onDragLeave={handleDragLeave}
        onDragOver={handleDragOver}
        onDrop={handleDrop}
        whileHover={{ scale: 1.02 }}
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24">
          <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8l-6-6z"/>
          <path d="M14 3v5h5m-5 4H9m2 4H9m4-8H9"/>
        </svg>
        <p>Drag & drop your resume here or click to browse</p>
        <p>PDF files only</p>
        {fileName && <p className="file-name">{fileName}</p>}
        {isUploading && <p>Uploading...</p>}
        {resumeId && <p>Resume ID: {resumeId}</p>}
      </UploadBox>

      <JobDescriptionInput
        placeholder="Paste the job description here..."
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />

      <MatchButton
        onClick={onMatchResume}
        disabled={!resumeId || !jobDescription.trim() || isProcessing}
        whileTap={{ scale: 0.95 }}
      >
        {isProcessing ? (
          <>
            <LoadingSpinner />
            Processing...
          </>
        ) : (
          'Analyze Match'
        )}
      </MatchButton>
    </UploadContainer>
  );
};

export default ResumeUploader;