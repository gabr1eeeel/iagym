import React from 'react';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import theme from './theme';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Alunos from './pages/Alunos';
import Checkin from './pages/Checkin';
import FrequenciaPage from './pages/Frequencia';
import Churn from './pages/Churn';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/alunos" element={<Alunos />} />
          <Route path="/checkin" element={<Checkin />} />
          <Route path="/frequencia" element={<FrequenciaPage />} />
          <Route path="/churn" element={<Churn />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
