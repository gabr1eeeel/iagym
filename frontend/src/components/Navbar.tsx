import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';

const Navbar: React.FC = () => {
  return (
    <AppBar position="static" sx={{ backgroundColor: 'transparent', boxShadow: 'none' }}>
      <Toolbar>
        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <FitnessCenterIcon sx={{ color: 'primary.main', mr: 1 }} />
          <Typography
            variant="h6"
            component={RouterLink}
            to="/"
            sx={{
              textDecoration: 'none',
              color: 'primary.main',
              fontWeight: 'bold',
            }}
          >
            IA Gym
          </Typography>
        </Box>
        <Box>
          <Button
            color="inherit"
            component={RouterLink}
            to="/alunos"
            sx={{ mx: 1 }}
          >
            Alunos
          </Button>
          <Button
            color="inherit"
            component={RouterLink}
            to="/checkin"
            sx={{ mx: 1 }}
          >
            Check-in
          </Button>
          <Button
            color="inherit"
            component={RouterLink}
            to="/frequencia"
            sx={{ mx: 1 }}
          >
            Frequência
          </Button>
          <Button
            color="inherit"
            component={RouterLink}
            to="/churn"
            sx={{ mx: 1 }}
          >
            Risco de Churn
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 