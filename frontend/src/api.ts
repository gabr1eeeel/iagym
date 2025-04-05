import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:8000',
});

export interface Plano {
  id: number;
  nome: string;
  preco: number;
  descricao: string;
}

export interface Aluno {
  id: number;
  nome: string;
  email: string;
  telefone: string;
  plano_id: number;
  data_matricula: string;
  nome_plano: string;
  risco_churn: number;
  status_matricula: string;
  data_cancelamento?: string;
}

export interface Checkin {
  id: number;
  aluno_id: number;
  data: string;
}

export interface Frequencia {
  total_dias: number;
  dias_presentes: number;
  percentual: number;
}

export interface RiscoChurn {
  risco: number;
  fatores: string[];
}

export interface NovoAluno {
  nome: string;
  email: string;
  telefone: string;
  plano_id: number;
  status_matricula: string;
}

export const apiService = {
  // Alunos
  listarAlunos: async () => {
    const response = await api.get<Aluno[]>('/aluno');
    return response.data;
  },

  listarPlanos: async () => {
    const response = await api.get<Plano[]>('/plano');
    return response.data;
  },

  inicializarPlanos: async () => {
    const response = await api.post('/plano/inicializar');
    return response.data;
  },

  criarAluno: async (aluno: NovoAluno) => {
    const response = await api.post<Aluno>('/aluno', aluno);
    return response.data;
  },

  // Checkins
  registrarCheckin: async (alunoId: number) => {
    const response = await api.post<Checkin>('/aluno/checkin/', { aluno_id: alunoId });
    return response.data;
  },

  // Frequência
  obterFrequencia: async (alunoId: number) => {
    const response = await api.get<Frequencia>(`/aluno/${alunoId}/frequencia/`);
    return response.data;
  },

  // Risco de Churn
  obterRiscoChurn: async (alunoId: number) => {
    const response = await api.get<RiscoChurn>(`/aluno/${alunoId}/risco-churn`);
    return response.data;
  },

  // Cancelar Matrícula
  cancelarMatricula: async (alunoId: number) => {
    const response = await api.post<Aluno>(`/aluno/${alunoId}/cancelar`);
    return response.data;
  },

  // Atualizar Aluno
  atualizarAluno: async (alunoId: number, aluno: Partial<Aluno>) => {
    const response = await api.put<Aluno>(`/aluno/${alunoId}`, aluno);
    return response.data;
  },

  // Deletar Aluno
  deletarAluno: async (alunoId: number) => {
    const response = await api.delete(`/aluno/${alunoId}`);
    return response.data;
  },
}; 