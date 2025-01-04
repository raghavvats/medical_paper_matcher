import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow,
  IconButton,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogContentText,
  DialogActions,
  Button,
  Card,
  CardContent
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const PaperManager = () => {
  const [papers, setPapers] = useState([]);
  const [error, setError] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [selectedPaper, setSelectedPaper] = useState(null);
  const [viewDialogOpen, setViewDialogOpen] = useState(false);
  const [pdfContent, setPdfContent] = useState(null);

  const fetchPapers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/papers`);
      setPapers(response.data);
    } catch (err) {
      setError('Failed to load papers');
    }
  };

  useEffect(() => {
    fetchPapers();
  }, []);

  const handleDelete = async (paperId) => {
    try {
      await axios.delete(`${API_BASE_URL}/papers/${paperId}`);
      await fetchPapers();
      setDeleteDialogOpen(false);
      setSelectedPaper(null);
    } catch (err) {
      setError('Failed to delete paper');
    }
  };

  const openDeleteDialog = (paper) => {
    setSelectedPaper(paper);
    setDeleteDialogOpen(true);
  };

  const viewPaper = async (paper) => {
    try {
      setSelectedPaper(paper);
      const response = await axios.get(`${API_BASE_URL}/papers/${paper._id}/view`);
      setPdfContent(response.data.pdf_content);
      setViewDialogOpen(true);
    } catch (err) {
      setError('Failed to load PDF');
      console.error('Error loading PDF:', err);
    }
  };

  return (
    <Box sx={{ 
      my: 4,
      backgroundColor: '#fff',
      borderRadius: '8px',
      padding: '20px'
    }}>
      <Typography variant="h5" gutterBottom>
        Manage Research Papers
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      <Card>
        <CardContent>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Title</TableCell>
                  <TableCell>Summary</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {papers.map((paper) => (
                  <TableRow key={paper._id}>
                    <TableCell>{paper.title}</TableCell>
                    <TableCell>{paper.processed_data.summary}</TableCell>
                    <TableCell align="right">
                      <IconButton 
                        onClick={() => viewPaper(paper)}
                        color="primary"
                      >
                        <VisibilityIcon />
                      </IconButton>
                      <IconButton 
                        onClick={() => openDeleteDialog(paper)}
                        color="error"
                      >
                        <DeleteIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete "{selectedPaper?.title}"?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button 
            onClick={() => handleDelete(selectedPaper?._id)} 
            color="error"
          >
            Delete
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog
        open={viewDialogOpen}
        onClose={() => {
          setViewDialogOpen(false);
          setPdfContent(null);
          setSelectedPaper(null);
        }}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: {
            height: '90vh',
            maxHeight: '90vh'
          }
        }}
      >
        <DialogTitle>
          {selectedPaper?.title}
        </DialogTitle>
        <DialogContent dividers>
          {selectedPaper && (
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
              <Box>
                <Typography variant="h6" gutterBottom>
                  Summary
                </Typography>
                <Typography>
                  {selectedPaper.processed_data.summary}
                </Typography>
              </Box>

              <Box>
                <Typography variant="h6" gutterBottom>
                  Ideal Profile
                </Typography>
                <pre style={{ 
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'inherit',
                  margin: 0
                }}>
                  {JSON.stringify(selectedPaper.processed_data.ideal_profile, null, 2)}
                </pre>
              </Box>

              <Box>
                <Typography variant="h6" gutterBottom>
                  Conditions
                </Typography>
                <pre style={{ 
                  whiteSpace: 'pre-wrap',
                  fontFamily: 'inherit',
                  margin: 0
                }}>
                  {JSON.stringify(selectedPaper.processed_data.conditions, null, 2)}
                </pre>
              </Box>

              {pdfContent && (
                <Box>
                  <Typography variant="h6" gutterBottom>
                    PDF Document
                  </Typography>
                  <Box sx={{ 
                    width: '100%', 
                    height: '80vh',
                    marginBottom: '20px'
                  }}>
                    <iframe
                      src={`data:application/pdf;base64,${pdfContent}`}
                      width="100%"
                      height="100%"
                      title="PDF Viewer"
                      style={{ border: 'none' }}
                    />
                  </Box>
                </Box>
              )}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => {
            setViewDialogOpen(false);
            setPdfContent(null);
            setSelectedPaper(null);
          }}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PaperManager; 