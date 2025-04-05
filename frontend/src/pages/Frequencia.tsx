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
  Grow,
  Snackbar,
} from '@mui/material';
import { apiService } from '../api';
import type { Frequencia as FrequenciaType } from '../api';

const FrequenciaPage: React.FC = () => {
  const [alunoId, setAlunoId] = useState<string>('');
  const [frequencia, setFrequencia] = useState<FrequenciaType | null>(null);
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
      const data = await apiService.obterFrequencia(parseInt(alunoId));
      setFrequencia(data);
    } catch (err) {
      setError('Erro ao consultar frequência. Verifique o ID do aluno.');
    } finally {
      setLoading(false);
    }
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
            Consultar Frequência
          </Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="ID do Aluno"
              value={alunoId}
              onChange={(e: React.ChangeEvent<HTMLInputElement>) => setAlunoId(e.target.value)}
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
              {loading ? <CircularProgress size={24} /> : 'Consultar Frequência'}
            </Button>
          </form>
        </CardContent>
      </Card>
      </Grow>

      {frequencia && (
        <Grow in timeout={800}>
        <Card sx={{ maxWidth: 600, mx: 'auto' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Resultados da Consulta
            </Typography>
            <Box sx={{ display: 'grid', gap: 2 }}>
              <Typography variant="body1">
                Total de Dias: {frequencia.total_dias}
              </Typography>
              <Typography variant="body1">
                Dias Presentes: {frequencia.dias_presentes}
              </Typography>
              <Typography variant="body1">
                Percentual de Frequência: {(frequencia.percentual * 100).toFixed(1)}%
              </Typography>
            </Box>
          </CardContent>
        </Card>
        </Grow>
      )}
    </Box>
  );
};

export default FrequenciaPage; 