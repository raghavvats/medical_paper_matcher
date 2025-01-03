import React from 'react';
import { Box, Card, CardContent, Typography, Link } from '@mui/material';

const MatchResults = ({ matches }) => {
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
            <Link href={match.download_url} target="_blank">
              Download Paper
            </Link>
          </CardContent>
        </Card>
      ))}
    </Box>
  );
};

export default MatchResults; 