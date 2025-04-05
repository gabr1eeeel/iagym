import React from 'react';
import { Box, Typography, Container, Grid, Paper, Button } from '@mui/material';
import { styled } from '@mui/material/styles';
import FitnessCenterIcon from '@mui/icons-material/FitnessCenter';
import PeopleIcon from '@mui/icons-material/People';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import AssessmentIcon from '@mui/icons-material/Assessment';
import { Link } from 'react-router-dom';

const StyledPaper = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(4),
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  textAlign: 'center',
  transition: 'transform 0.3s ease, box-shadow 0.3s ease',
  '&:hover': {
    transform: 'translateY(-8px)',
    boxShadow: '0 8px 24px rgba(0, 0, 0, 0.1)',
  },
}));

const IconWrapper = styled(Box)(({ theme }) => ({
  width: '80px',
  height: '80px',
  borderRadius: '50%',
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  marginBottom: theme.spacing(3),
  background: 'linear-gradient(45deg, #d32f2f 30%, #f44336 90%)',
  color: 'white',
}));

const StyledButton = styled(Button)(({ theme }) => ({
  marginTop: theme.spacing(2),
  borderRadius: '20px',
  padding: '8px 24px',
})) as typeof Button;

const Home = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ textAlign: 'center', mb: 6 }}>
        <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 'bold', color: 'primary.main', mt: 4 }}>
          Bem-vindo ao IAGym
        </Typography>
        <Typography variant="h6" color="text.secondary" sx={{ maxWidth: '600px', mx: 'auto' }}>
          Sistema inteligente de gestão para academias
        </Typography>
      </Box>

      <Grid container spacing={4}>
        <Grid item xs={12} sm={6} md={3}>
          <StyledPaper elevation={3}>
            <IconWrapper>
              <PeopleIcon sx={{ fontSize: 40 }} />
            </IconWrapper>
            <Typography variant="h5" gutterBottom>
              Alunos
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Gerencie seus alunos e acompanhe seu progresso
            </Typography>
            <StyledButton
              variant="contained"
              component={Link}
              to="/alunos"
              startIcon={<PeopleIcon />}
            >
              Acessar
            </StyledButton>
          </StyledPaper>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StyledPaper elevation={3}>
            <IconWrapper>
              <TrendingUpIcon sx={{ fontSize: 40 }} />
            </IconWrapper>
            <Typography variant="h5" gutterBottom>
              Check-in
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Registre a frequência dos alunos
            </Typography>
            <StyledButton
              variant="contained"
              component={Link}
              to="/checkin"
              startIcon={<TrendingUpIcon />}
            >
              Acessar
            </StyledButton>
          </StyledPaper>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StyledPaper elevation={3}>
            <IconWrapper>
              <AssessmentIcon sx={{ fontSize: 40 }} />
            </IconWrapper>
            <Typography variant="h5" gutterBottom>
              Churn
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Analise o risco de evasão dos alunos
            </Typography>
            <StyledButton
              variant="contained"
              component={Link}
              to="/churn"
              startIcon={<AssessmentIcon />}
            >
              Acessar
            </StyledButton>
          </StyledPaper>
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <StyledPaper elevation={3}>
            <IconWrapper>
              <FitnessCenterIcon sx={{ fontSize: 40 }} />
            </IconWrapper>
            <Typography variant="h5" gutterBottom>
              Métricas
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Visualize métricas e indicadores importantes
            </Typography>
            <StyledButton
              variant="contained"
              component={Link}
              to="/frequencia"
              startIcon={<FitnessCenterIcon />}
            >
              Acessar
            </StyledButton>
          </StyledPaper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default Home; 