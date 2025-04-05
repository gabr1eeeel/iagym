import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  TextField,
  Alert,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
  Grow,
  Zoom,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import { apiService, Aluno, Plano } from '../api';

const Alunos: React.FC = () => {
  const [alunos, setAlunos] = useState<Aluno[]>([]);
  const [planos, setPlanos] = useState<Plano[]>([]);
  const [novoAluno, setNovoAluno] = useState({
    nome: '',
    email: '',
    telefone: '',
    plano_id: '',
  });
  const [alunoEditando, setAlunoEditando] = useState<Aluno | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [alunoParaExcluir, setAlunoParaExcluir] = useState<Aluno | null>(null);
  const [dialogAberto, setDialogAberto] = useState(false);
  const [dialogEdicaoAberto, setDialogEdicaoAberto] = useState(false);

  useEffect(() => {
    const carregarDados = async () => {
      try {
        const [alunosData, planosData] = await Promise.all([
          apiService.listarAlunos(),
          apiService.listarPlanos(),
        ]);
        // Se não houver planos, inicializa
        if (planosData.length === 0) {
          await apiService.inicializarPlanos();
          const planosAtualizados = await apiService.listarPlanos();
          setPlanos(planosAtualizados);
        } else {
          setPlanos(planosData);
        }

        setAlunos(alunosData);
      } catch (err) {
        setError('Erro ao carregar dados.');
      }
    };
    carregarDados();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const aluno = await apiService.criarAluno({
        ...novoAluno,
        plano_id: parseInt(novoAluno.plano_id),
      });
      setAlunos([...alunos, aluno]);
      setNovoAluno({ nome: '', email: '', telefone: '', plano_id: '' });
      setSuccess('Aluno cadastrado com sucesso!');
      setError(null);
    } catch (err: any) {
      if (err.response?.data?.detail === 'Email já cadastrado') {
        setError('Este email já está cadastrado. Por favor, use outro email.');
      } else {
        setError('Erro ao cadastrar aluno. Tente novamente.');
      }
      setSuccess(null);
    }
  };

  const handleExcluirAluno = async () => {
    if (!alunoParaExcluir) return;

    try {
      await apiService.excluirAluno(alunoParaExcluir.id);
      setAlunos(alunos.filter(a => a.id !== alunoParaExcluir.id));
      setSuccess(`Aluno ${alunoParaExcluir.nome} excluído com sucesso!`);
      setAlunoParaExcluir(null);
      setDialogAberto(false);
    } catch (err) {
      setError('Erro ao excluir aluno. Tente novamente.');
    }
  };

  const handleEditarAluno = async () => {
    if (!alunoEditando) return;

    try {
      const alunoAtualizado = await apiService.atualizarAluno(alunoEditando.id, {
        nome: alunoEditando.nome,
        email: alunoEditando.email,
        telefone: alunoEditando.telefone,
        plano_id: alunoEditando.plano_id,
      });
      
      setAlunos(alunos.map(a => a.id === alunoAtualizado.id ? alunoAtualizado : a));
      setSuccess(`Aluno ${alunoAtualizado.nome} atualizado com sucesso!`);
      setAlunoEditando(null);
      setDialogEdicaoAberto(false);
    } catch (err) {
      setError('Erro ao atualizar aluno. Tente novamente.');
    }
  };

  return (
    <Box sx={{ p: 4 }}>
      {error && (
        <Zoom in>
          <Alert severity="error" sx={{ mb: 2 }}>
            {error}
          </Alert>
        </Zoom>
      )}

      {success && (
        <Zoom in>
          <Alert severity="success" sx={{ mb: 2 }}>
            {success}
          </Alert>
        </Zoom>
      )}

      <Grow in timeout={800}>
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Cadastrar Novo Aluno
            </Typography>
            <form onSubmit={handleSubmit}>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Nome"
                    value={novoAluno.nome}
                    onChange={(e) => setNovoAluno({ ...novoAluno, nome: e.target.value })}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Email"
                    type="email"
                    value={novoAluno.email}
                    onChange={(e) => setNovoAluno({ ...novoAluno, email: e.target.value })}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Telefone"
                    value={novoAluno.telefone}
                    onChange={(e) => setNovoAluno({ ...novoAluno, telefone: e.target.value })}
                    required
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth required>
                    <InputLabel id="plano-label">Plano</InputLabel>
                    <Select
                      labelId="plano-label"
                      value={novoAluno.plano_id}
                      onChange={(e) => {
                        setNovoAluno({ ...novoAluno, plano_id: e.target.value });
                      }}
                      label="Plano"
                    >
                      {planos.length > 0 ? (
                        planos.map((plano) => (
                          <MenuItem key={plano.id} value={plano.id}>
                            {plano.nome} - R$ {plano.preco}/mês
                          </MenuItem>
                        ))
                      ) : (
                        <MenuItem disabled>Carregando planos...</MenuItem>
                      )}
                    </Select>
                  </FormControl>
                </Grid>
                <Grid item xs={12}>
                  <Button type="submit" variant="contained" color="primary">
                    Cadastrar Aluno
                  </Button>
                </Grid>
              </Grid>
            </form>
          </CardContent>
        </Card>
      </Grow>

      <Typography variant="h6" gutterBottom>
        Alunos Cadastrados
      </Typography>
      <Grid container spacing={2}>
        {alunos.map((aluno, index) => (
          <Grid item xs={12} sm={6} md={4} key={aluno.id}>
            <Grow in timeout={500 + index * 100}>
              <Card>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <Typography variant="h6">{aluno.nome}</Typography>
                    <Box>
                      <IconButton
                        color="primary"
                        onClick={() => {
                          setAlunoEditando(aluno);
                          setDialogEdicaoAberto(true);
                        }}
                      >
                        <EditIcon />
                      </IconButton>
                      <IconButton
                        color="error"
                        onClick={() => {
                          setAlunoParaExcluir(aluno);
                          setDialogAberto(true);
                        }}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </Box>
                  <Typography color="textSecondary">ID: {aluno.id}</Typography>
                  <Typography color="textSecondary">{aluno.email}</Typography>
                  <Typography color="textSecondary">{aluno.telefone}</Typography>
                  <Typography color="textSecondary">
                    Plano: {aluno.nome_plano}
                  </Typography>
                  <Typography color="textSecondary">
                    Data de Matrícula: {new Date(aluno.data_matricula).toLocaleDateString()}
                  </Typography>
                </CardContent>
              </Card>
            </Grow>
          </Grid>
        ))}
      </Grid>

      <Dialog open={dialogAberto} onClose={() => setDialogAberto(false)}>
        <DialogTitle>Confirmar Exclusão</DialogTitle>
        <DialogContent>
          <Typography>
            Tem certeza que deseja excluir o aluno {alunoParaExcluir?.nome}?
            Esta ação não pode ser desfeita e excluirá todos os dados associados ao aluno.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogAberto(false)}>Cancelar</Button>
          <Button onClick={handleExcluirAluno} color="error" variant="contained">
            Excluir
          </Button>
        </DialogActions>
      </Dialog>

      <Dialog open={dialogEdicaoAberto} onClose={() => setDialogEdicaoAberto(false)}>
        <DialogTitle>Editar Aluno</DialogTitle>
        <DialogContent>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2, mt: 2 }}>
            <TextField
              fullWidth
              label="Nome"
              value={alunoEditando?.nome || ''}
              onChange={(e) => setAlunoEditando({ ...alunoEditando!, nome: e.target.value })}
              required
            />
            <TextField
              fullWidth
              label="Email"
              type="email"
              value={alunoEditando?.email || ''}
              onChange={(e) => setAlunoEditando({ ...alunoEditando!, email: e.target.value })}
              required
            />
            <TextField
              fullWidth
              label="Telefone"
              value={alunoEditando?.telefone || ''}
              onChange={(e) => setAlunoEditando({ ...alunoEditando!, telefone: e.target.value })}
              required
            />
            <FormControl fullWidth required>
              <InputLabel id="plano-edit-label">Plano</InputLabel>
              <Select
                labelId="plano-edit-label"
                value={alunoEditando?.plano_id || ''}
                onChange={(e) => setAlunoEditando({ ...alunoEditando!, plano_id: Number(e.target.value) })}
                label="Plano"
              >
                {planos.map((plano) => (
                  <MenuItem key={plano.id} value={plano.id}>
                    {plano.nome} - R$ {plano.preco}/mês
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogEdicaoAberto(false)}>Cancelar</Button>
          <Button onClick={handleEditarAluno} color="primary" variant="contained">
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Alunos; 