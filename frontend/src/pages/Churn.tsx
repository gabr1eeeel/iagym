import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  TextField,
  Alert,
  CircularProgress,
  LinearProgress,
  List,
  ListItem,
  ListItemText,
  Grow,
  Snackbar,
} from '@mui/material';
import { apiService, RiscoChurn } from '../api';

const Churn: React.FC = () => {
  const [alunoId, setAlunoId] = useState<string>('');
  const [riscoChurn, setRiscoChurn] = useState<RiscoChurn | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [openError, setOpenError] = useState(false);

  const handleCloseError = () => {
    setOpenError(false);
    setError(null);
  };

  useEffect(() => {
    if (error) {
      setOpenError(true);
    }
  }, [error]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const data = await apiService.obterRiscoChurn(parseInt(alunoId));
      setRiscoChurn(data);
    } catch (err) {
      setError('Erro ao consultar risco de churn. Verifique o ID do aluno.');
    } finally {
      setLoading(false);
    }
  };

  const getRiskColor = (probability: number) => {
    if (probability < 0.3) return 'success';
    if (probability < 0.7) return 'warning';
    return 'error';
  };

  return (
    <Box sx={{ p: 4 }}>
      <Snackbar
        open={openError}
        autoHideDuration={3000}
        onClose={handleCloseError}
      >
        <Alert onClose={handleCloseError} severity="error" sx={{ width: '100%' }}>
          {error}
        </Alert>
      </Snackbar>

      <Grow in timeout={800}>
      <Card sx={{ maxWidth: 600, mx: 'auto', mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Consultar Risco de Churn
          </Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="ID do Aluno"
              value={alunoId}
              onChange={(e) => setAlunoId(e.target.value)}
              required
              sx={{ mb: 2 }}
              inputProps={{
                inputMode: 'numeric',
                pattern: '[0-9]*'
              }}
            />
            <Button
              type="submit"
              variant="contained"
              color="primary"
              fullWidth
              disabled={loading}
            >
              {loading ? <CircularProgress size={24} /> : 'Consultar Risco'}
            </Button>
          </form>
        </CardContent>
      </Card>
      </Grow>

      {riscoChurn && (
        <Grow in timeout={800}>
        <Card sx={{ maxWidth: 600, mx: 'auto' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Resultados da Análise
            </Typography>
            <Box sx={{ display: 'grid', gap: 2 }}>
              <Box>
                <Typography gutterBottom>
                  Probabilidade de Churn: {(riscoChurn.risco * 100).toFixed(1)}%
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={riscoChurn.risco * 100}
                  color={getRiskColor(riscoChurn.risco)}
                  sx={{ height: 10, borderRadius: 5 }}
                />
              </Box>
              <Box>
                {riscoChurn.fatores.length > 0 ? (
                  <Typography variant="subtitle1" gutterBottom>
                    Fatores de Risco:
                  </Typography>
                ) : (
                  <Typography variant="subtitle1" gutterBottom>
                    Nenhum fator de risco identificado
                  </Typography>
                )}
                <List>
                  {riscoChurn.fatores.map((fator, index) => (
                    <ListItem key={index}>
                      <ListItemText primary={fator} />
                    </ListItem>
                  ))}
                </List>
              </Box>
            </Box>
          </CardContent>
        </Card>
        </Grow>
      )}
    </Box>
  );
};

export default Churn; 