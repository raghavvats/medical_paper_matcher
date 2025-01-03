import React, { useState, useEffect } from 'react';
import { Dialog, DialogContent, IconButton, CircularProgress, Box, Typography } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

const PdfViewer = ({ pdfContent, open, onClose }) => {
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [blobUrl, setBlobUrl] = useState(null);

  useEffect(() => {
    if (pdfContent) {
      try {
        // Convert base64 to Blob
        const byteCharacters = atob(pdfContent);
        const byteNumbers = new Array(byteCharacters.length);
        for (let i = 0; i < byteCharacters.length; i++) {
          byteNumbers[i] = byteCharacters.charCodeAt(i);
        }
        const byteArray = new Uint8Array(byteNumbers);
        const blob = new Blob([byteArray], { type: 'application/pdf' });
        
        // Create blob URL
        const url = URL.createObjectURL(blob);
        setBlobUrl(url);
        setIsLoading(false);
      } catch (err) {
        console.error('Error creating PDF blob:', err);
        setError('Failed to process PDF data');
        setIsLoading(false);
      }
    }

    // Cleanup
    return () => {
      if (blobUrl) {
        URL.revokeObjectURL(blobUrl);
      }
    };
  }, [pdfContent]);

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="lg"
      fullWidth
      PaperProps={{
        sx: {
          height: '90vh',
          bgcolor: 'background.paper',
        }
      }}
    >
      <IconButton
        onClick={onClose}
        sx={{
          position: 'absolute',
          right: 8,
          top: 8,
          color: 'grey.500',
          zIndex: 1,
        }}
      >
        <CloseIcon />
      </IconButton>
      <DialogContent sx={{ p: 0, height: '100%', position: 'relative' }}>
        {isLoading && (
          <Box
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              textAlign: 'center',
            }}
          >
            <CircularProgress />
            <Typography sx={{ mt: 2 }}>Loading PDF...</Typography>
          </Box>
        )}
        
        {error && (
          <Box
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
              textAlign: 'center',
              color: 'error.main',
            }}
          >
            <Typography>{error}</Typography>
          </Box>
        )}

        {blobUrl && !isLoading && !error && (
          <iframe
            src={blobUrl}
            width="100%"
            height="100%"
            style={{ border: 'none' }}
            title="PDF Viewer"
          />
        )}
      </DialogContent>
    </Dialog>
  );
};

export default PdfViewer; 