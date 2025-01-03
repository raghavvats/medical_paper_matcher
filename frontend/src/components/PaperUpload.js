import React, { useState } from 'react';
import { Box, Button, Typography } from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import axios from 'axios';

const PaperUpload = () => {
  const [uploading, setUploading] = useState(false);

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    setUploading(true);
    try {
      const response = await axios.post('http://localhost:8000/papers/upload/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Upload successful:', response.data);
    } catch (error) {
      console.error('Upload failed:', error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Box sx={{ textAlign: 'center' }}>
      <input
        accept="application/pdf"
        style={{ display: 'none' }}
        id="raised-button-file"
        type="file"
        onChange={handleFileUpload}
      />
      <label htmlFor="raised-button-file">
        <Button
          variant="contained"
          component="span"
          disabled={uploading}
          startIcon={<CloudUploadIcon />}
          sx={{
            py: 1.5,
            px: 4,
            backgroundColor: '#2196f3',
            '&:hover': {
              backgroundColor: '#1976d2',
            }
          }}
        >
          {uploading ? 'Uploading...' : 'Upload Paper'}
        </Button>
      </label>
      <Typography variant="body2" color="text.secondary" sx={{ mt: 2 }}>
        Upload PDF files to add to the research database
      </Typography>
    </Box>
  );
};

export default PaperUpload; 