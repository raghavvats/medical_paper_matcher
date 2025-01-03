import React, { useState } from 'react';
import { Container, Box, Typography, Card, CardContent } from '@mui/material';
import ProfileForm from './components/ProfileForm';
import PaperUpload from './components/PaperUpload';
import MatchResults from './components/MatchResults';

function App() {
  const [matches, setMatches] = useState(null);
  const [currentProfile, setCurrentProfile] = useState(null);

  return (
    <Container maxWidth="md">
      <Box sx={{ my: 4 }}>
        <Typography 
          variant="h3" 
          component="h1" 
          gutterBottom
          sx={{ color: '#fff' }}
        >
          Research Paper Matcher
        </Typography>
        
        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Upload Papers
            </Typography>
            <PaperUpload />
          </CardContent>
        </Card>

        <Card sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h5" gutterBottom>
              Enter Profile
            </Typography>
            <ProfileForm 
              onProfileSubmit={(profile) => setCurrentProfile(profile)}
              onMatchResults={(results) => setMatches(results)}
            />
          </CardContent>
        </Card>

        {matches && (
          <Card>
            <CardContent>
              <Typography variant="h5" gutterBottom>
                Matching Results
              </Typography>
              <MatchResults matches={matches} />
            </CardContent>
          </Card>
        )}
      </Box>
    </Container>
  );
}

export default App; 