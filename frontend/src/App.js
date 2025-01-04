import React from 'react';
import { HashRouter as Router, Route, Routes } from 'react-router-dom';
import { Container } from '@mui/material';
import Header from './components/Header';
import MatcherPage from './pages/MatcherPage';
import PaperManager from './components/PaperManager';

function App() {
  return (
    <Router>
      <Header />
      <Container maxWidth="lg">
        <Routes>
          <Route path="/" element={<MatcherPage />} />
          <Route path="/papers" element={<PaperManager />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App; 