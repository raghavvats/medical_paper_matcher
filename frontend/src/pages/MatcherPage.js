import React, { useState } from 'react';
import { Box, Typography, Card, CardContent } from '@mui/material';
import ProfileForm from '../components/ProfileForm';
import PaperUpload from '../components/PaperUpload';
import MatchResults from '../components/MatchResults';

const MatcherPage = () => {
  const [matches, setMatches] = useState(null);
  const [currentProfile, setCurrentProfile] = useState(null);

  return (
    <Box sx={{ 
      my: 4,
      backgroundColor: '#fff',
      borderRadius: '8px',
      padding: '20px'
    }}>
      <Typography 
        variant="h4" 
        component="h1" 
        gutterBottom
        sx={{ color: '#000' }}
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
  );
};

export default MatcherPage; 