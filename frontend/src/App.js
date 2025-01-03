import React, { useState } from 'react';
import { Container, Box, Typography } from '@mui/material';
import ProfileForm from './components/ProfileForm';
import PaperUpload from './components/PaperUpload';
import MatchResults from './components/MatchResults';

function App() {
  const [matches, setMatches] = useState(null);
  const [currentProfile, setCurrentProfile] = useState(null);

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Research Paper Matcher
        </Typography>
        
        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" gutterBottom>
            Upload Papers
          </Typography>
          <PaperUpload />
        </Box>

        <Box sx={{ mb: 4 }}>
          <Typography variant="h5" gutterBottom>
            Enter Profile
          </Typography>
          <ProfileForm 
            onProfileSubmit={(profile) => setCurrentProfile(profile)}
            onMatchResults={(results) => setMatches(results)}
          />
        </Box>

        {matches && (
          <Box sx={{ mb: 4 }}>
            <Typography variant="h5" gutterBottom>
              Matching Results
            </Typography>
            <MatchResults matches={matches} />
          </Box>
        )}
      </Box>
    </Container>
  );
}

export default App; 