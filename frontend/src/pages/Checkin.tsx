import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  TextField,
  Alert,
} from '@mui/material';
import { apiService } from '../api';

const Checkin: React.FC = () => {
  const [alunoId, setAlunoId] = useState<string>('');
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

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
      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {success && (
        <Alert severity="success" sx={{ mb: 2 }}>
          {success}
        </Alert>
      )}

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
    </Box>
  );
};

export default Checkin; 