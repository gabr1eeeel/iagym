# IAGym - Sistema Inteligente de Gestão para Academias

## 📋 Índice
- [Visão Geral](#visão-geral)
- [Funcionalidades](#funcionalidades)
- [Arquitetura](#arquitetura)
- [Tecnologias](#tecnologias)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Contribuição](#contribuição)
- [Licença](#licença)

## 🎯 Visão Geral

IAGym é um sistema de gestão inteligente para academias que combina análise de dados e machine learning para otimizar a experiência dos alunos e aumentar a retenção. O sistema utiliza um modelo de Random Forest para prever o risco de cancelamento (churn) dos alunos, analisando padrões de frequência, engajamento e comportamento.

Este projeto foi desenvolvido utilizando **Vibe Coding**, uma técnica de programação que utiliza inteligência artificial para construir software. O diferencial está no modelo de machine learning que analisa diversos fatores para prever o risco de cancelamento, incluindo:
- Frequência semanal e mensal
- Padrões de inatividade
- Regularidade dos treinos
- Histórico de engajamento
- Tempo de matrícula
- Características do plano

![Visão Geral do Sistema](/.github/assets/gifs/home.gif)

## ✨ Funcionalidades

### 👤 Gestão de Alunos
- Cadastro completo de alunos
- Edição de informações
- Exclusão de registros
- Visualização detalhada do perfil

### Cadastro e Edição de Alunos
![Interface de cadastro e edição de informações dos alunos, permitindo atualizar dados pessoais e do plano](/.github/assets/gifs/cadastroeedicaoaluno.gif)

### Processo de Exclusão de Alunos
![Demonstração do processo seguro de exclusão de alunos do sistema](/.github/assets/gifs/excluindoaluno.gif)

### 📊 Análise de Frequência
- Registro de check-in
- Consulta de histórico de frequência
- Visualização de métricas de presença
- Cálculo de percentual de frequência nos últimos 30 dias

### Registro de Check-in de Alunos
![Sistema de registro de check-in dos alunos na academia](/.github/assets/gifs/cadastrarcheckin.gif)

### Consulta de Histórico de Frequência
![Visualização detalhada do histórico de frequência e métricas de presença](/.github/assets/gifs/consultarfrequencia.gif)

### 🔮 Análise de Churn com Machine Learning
- Predição de risco de cancelamento usando Random Forest
- Identificação de fatores de risco específicos por aluno
- Atualização automática do modelo a cada 10 check-ins
- Análise de múltiplas variáveis:
  - Frequência semanal (últimos 7 dias)
  - Frequência mensal (últimos 30 dias)
  - Dias desde o último check-in
  - Variância entre check-ins (regularidade)
  - Tempo de matrícula
  - Média histórica de check-ins
  - Valor do plano

### Consulta de Risco de Churn
![Análise detalhada do risco de cancelamento de matrícula do aluno](/.github/assets/gifs/consultarchurn.gif)

### Atualização da Análise de Churn
![Processo de atualização e recálculo do risco de churn baseado em novos dados](/.github/assets/gifs/churnatualizando.gif)

### 💳 Gestão de Planos
- Cadastro de planos
- Configuração de preços
- Planos pré-definidos (Básico, Premium, VIP)
- Associação de alunos a planos

## 🏗️ Arquitetura

O sistema é construído com uma arquitetura moderna e escalável:

```
IAGym/
├── backend/
│   ├── app/
│   │   ├── routes/        # Endpoints REST
│   │   ├── models/        # Modelos de dados
│   │   ├── services/      # Serviços de negócio
│   │   └── ml_models/     # Modelos de machine learning
│   └── tests/             # Testes automatizados
├── frontend/
└── docker/                # Configurações Docker
```

## 🛠️ Tecnologias

### Backend
- **Python**: Linguagem principal
- **FastAPI**: Framework web para APIs
- **SQLAlchemy**: ORM para banco de dados
- **PostgreSQL**: Banco de dados relacional
- **scikit-learn**: Biblioteca de machine learning
- **numpy**: Processamento numérico
- **RabbitMQ**: Message broker para processamento assíncrono

### Frontend
- **React**: Biblioteca UI
- **TypeScript**: Tipagem estática
- **Material-UI**: Componentes de interface

### DevOps
- **Docker**: Containerização
- **Docker Compose**: Orquestração de containers

## 🚀 Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/iagym.git
cd iagym
```

2. Configure as variáveis de ambiente:
```bash
cp backend/.env.example backend/.env
```

Variáveis necessárias:
```env
DATABASE_URL=postgresql://user:password@db:5432/iagym
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
```

3. Inicie os containers:
```bash
docker-compose up -d
```

4. Inicialize os planos padrão:
```bash
curl -X POST http://localhost:8000/planos/inicializar
```

5. Acesse a aplicação:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- Documentação: http://localhost:8000/docs

## 📖 Uso

### API Endpoints

#### Alunos
- `GET /alunos/`: Lista todos os alunos
- `POST /alunos/`: Cadastra novo aluno
- `PUT /alunos/{aluno_id}`: Atualiza aluno
- `DELETE /alunos/{aluno_id}`: Remove aluno
- `GET /alunos/{aluno_id}/frequencia`: Histórico de frequência
- `GET /alunos/{aluno_id}/risco-churn`: Análise de risco de churn
- `POST /alunos/{aluno_id}/cancelar`: Cancela matrícula do aluno

#### Check-ins
- `POST /checkin/`: Registra check-in

#### Planos
- `GET /planos/`: Lista todos os planos
- `POST /planos/`: Cadastra novo plano
- `GET /planos/{plano_id}`: Detalhes do plano
- `POST /planos/inicializar`: Inicializa planos padrão

### Processamento Assíncrono

O sistema utiliza RabbitMQ para processamento assíncrono de eventos:

1. **Check-ins em Lote**:
   - Fila: `checkins`
   - Routing Key: `gym.checkins.*`

2. **Análise de Churn**:
   - Fila: `churn_analysis`
   - Routing Key: `gym.churn.*`

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.
