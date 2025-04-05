import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  TextField,
  Alert,
  Grow,
  Snackbar,
} from '@mui/material';
import { apiService } from '../api';

const Checkin: React.FC = () => {
  const [alunoId, setAlunoId] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [openError, setOpenError] = useState(false);
  const [openSuccess, setOpenSuccess] = useState(false);

  const handleCloseError = () => {
    setOpenError(false);
    setError(null);
  };

  const handleCloseSuccess = () => {
    setOpenSuccess(false);
    setSuccess(null);
  };

  useEffect(() => {
    if (error) {
      setOpenError(true);
    }
  }, [error]);

  useEffect(() => {
    if (success) {
      setOpenSuccess(true);
    }
  }, [success]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiService.registrarCheckin(parseInt(alunoId));
      setAlunoId('');
      setSuccess('Check-in registrado com sucesso!');
      setError(null);
    } catch (err) {
      setError('Erro ao registrar check-in. Verifique o ID do aluno.');
      setSuccess(null);
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

      <Snackbar
        open={openSuccess}
        autoHideDuration={3000}
        onClose={handleCloseSuccess}
      >
        <Alert onClose={handleCloseSuccess} severity="success" sx={{ width: '100%' }}>
          {success}
        </Alert>
      </Snackbar>

      <Grow in timeout={800}>
        <Card sx={{ maxWidth: 600, mx: 'auto' }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
            Registrar Check-in
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
            <Button type="submit" variant="contained" color="primary" fullWidth>
              Registrar Check-in
            </Button>
          </form>
          </CardContent>
        </Card>
      </Grow>
    </Box>
  );
};

export default Checkin; 