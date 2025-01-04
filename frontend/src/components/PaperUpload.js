import React, { useState, useRef } from 'react';
import { Box, Button, Typography, LinearProgress, Alert } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const PaperUpload = () => {
  const [uploading, setUploading] = useState(false);
  const [uploadResults, setUploadResults] = useState([]);
  const fileInputRef = useRef(null);

  const handleUpload = async (event) => {
    const files = event.target.files;
    if (files.length === 0) return;

    setUploading(true);
    setUploadResults([]);

    const formData = new FormData();
    Array.from(files).forEach(file => {
      formData.append('files', file);
    });

    try {
      const response = await axios.post(`${API_BASE_URL}/papers/upload/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setUploadResults(response.data);
    } catch (error) {
      setUploadResults([{
        title: 'Upload Error',
        message: error.message,
        success: false
      }]);
    } finally {
      setUploading(false);
      // Reset file input
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <Box>
      <input
        type="file"
        accept=".pdf"
        multiple
        onChange={handleUpload}
        style={{ display: 'none' }}
        ref={fileInputRef}
      />
      
      <Box sx={{ 
        display: 'flex', 
        flexDirection: 'column', 
        alignItems: 'center',
        p: 3,
        border: '2px dashed #ccc',
        borderRadius: 2,
        bgcolor: '#fafafa',
        cursor: 'pointer'
      }} onClick={() => fileInputRef.current?.click()}>
        <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
        <Typography variant="h6" gutterBottom>
          Click to Upload PDFs
        </Typography>
        <Typography variant="body2" color="textSecondary">
          Select one or more PDF files
        </Typography>
      </Box>

      {uploading && (
        <Box sx={{ mt: 2 }}>
          <LinearProgress />
          <Typography sx={{ mt: 1 }} align="center">
            Processing papers...
          </Typography>
        </Box>
      )}

      {uploadResults.length > 0 && (
        <Box sx={{ mt: 2 }}>
          {uploadResults.map((result, index) => (
            <Alert 
              key={index}
              severity={result.paper_id ? "success" : "error"}
              sx={{ mb: 1 }}
            >
              {result.title}: {result.message}
            </Alert>
          ))}
        </Box>
      )}
    </Box>
  );
};

export default PaperUpload; 