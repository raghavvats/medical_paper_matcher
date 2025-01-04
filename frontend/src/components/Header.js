import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const location = useLocation();

  return (
    <AppBar 
      position="static" 
      sx={{ 
        mb: 3,
        bgcolor: '#222222'
      }}
    >
      <Toolbar>
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          TEMP
        </Typography>
        <Box>
          <Button 
            color="inherit" 
            component={Link} 
            to="/"
            sx={{
              backgroundColor: location.pathname === '/' ? 'rgba(255, 255, 255, 0.12)' : 'transparent'
            }}
          >
            Matcher
          </Button>
          <Button 
            color="inherit" 
            component={Link} 
            to="/papers"
            sx={{
              backgroundColor: location.pathname === '/papers' ? 'rgba(255, 255, 255, 0.12)' : 'transparent'
            }}
          >
            Manage Papers
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header; 