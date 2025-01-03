import React, { useState } from 'react';
import { Box, Card, CardContent, Typography, Button, Snackbar, Alert } from '@mui/material';
import PictureAsPdfIcon from '@mui/icons-material/PictureAsPdf';
import axios from 'axios';
import PdfViewer from './PdfViewer';

const MatchResults = ({ matches }) => {
  const [selectedPdf, setSelectedPdf] = useState(null);
  const [pdfDialogOpen, setPdfDialogOpen] = useState(false);
  const [error, setError] = useState(null);

  const handleViewPdf = async (paperId) => {
    try {
      console.log('Fetching PDF for paper:', paperId);
      const response = await axios.get(`http://localhost:8000/papers/${paperId}/view`);
      console.log('PDF response:', response.data);
      
      if (response.data && response.data.pdf_content) {
        console.log('PDF content length:', response.data.pdf_content.length);
        setSelectedPdf(response.data.pdf_content);
        setPdfDialogOpen(true);
      } else {
        console.error('Invalid PDF response:', response.data);
        throw new Error('Invalid PDF data received');
      }
    } catch (error) {
      console.error('Error loading PDF:', error);
      setError('Failed to load PDF. Please try again.');
    }
  };

  const handleCloseError = () => {
    setError(null);
  };

  return (
    <Box>
      {matches.matches.map((match) => (
        <Card key={match.paper_id} sx={{ mb: 2 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              {match.title}
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              {match.summary}
            </Typography>
            <Button
              startIcon={<PictureAsPdfIcon />}
              onClick={() => handleViewPdf(match.paper_id)}
              variant="outlined"
              size="small"
            >
              View PDF
            </Button>
          </CardContent>
        </Card>
      ))}

      <PdfViewer
        pdfContent={selectedPdf}
        open={pdfDialogOpen}
        onClose={() => {
          setPdfDialogOpen(false);
          setSelectedPdf(null);
        }}
      />

      <Snackbar 
        open={!!error} 
        autoHideDuration={6000} 
        onClose={handleCloseError}
      >
        <Alert onClose={handleCloseError} severity="error">
          {error}
        </Alert>
      </Snackbar>
    </Box>
  );
};

export default MatchResults; 