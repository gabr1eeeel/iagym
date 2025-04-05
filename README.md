# IAGym - Sistema Inteligente de Gestão para Academias

![Logo do IAGym](assets/logo.png)

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

IAGym é um sistema de gestão inteligente para academias que combina análise de dados, machine learning e processamento em tempo real para otimizar a experiência dos alunos e aumentar a retenção. O sistema utiliza técnicas avançadas de análise de churn e processamento de eventos para fornecer insights valiosos sobre o comportamento dos alunos.

Este projeto foi desenvolvido utilizando **Vibe Coding**, uma técnica de programação que utiliza inteligência artificial para construir software. O processo envolve descrever as funcionalidades desejadas em linguagem natural e utilizar ferramentas de IA para gerar o código, resultando em um desenvolvimento mais rápido e eficiente.

## ✨ Funcionalidades

### 👤 Gestão de Alunos
- Cadastro completo de alunos
- Histórico de matrículas
- Gestão de planos e assinaturas
- Perfil individual com métricas de engajamento

![Demonstração do cadastro de alunos](assets/gifs/aluno-cadastro.gif)

### 📊 Análise de Frequência
- Dashboard de frequência em tempo real
- Relatórios personalizados
- Alertas de baixa frequência
- Análise de padrões de uso

![Demonstração da análise de frequência](assets/gifs/frequencia-analise.gif)

### 🔮 Previsão de Churn
- Modelo de machine learning para previsão de cancelamentos
- Identificação de alunos em risco
- Recomendações personalizadas
- Métricas de retenção

![Demonstração da previsão de churn](assets/gifs/churn-prediction.gif)

### 📱 Check-in Inteligente
- Sistema de check-in automatizado
- Processamento em lote
- Validação de presença
- Histórico detalhado

![Demonstração do sistema de check-in](assets/gifs/checkin-system.gif)

## 🏗️ Arquitetura

O sistema é construído com uma arquitetura moderna e escalável:

```
IAGym/
├── backend/
│   ├── app/
│   │   ├── routes/        # Endpoints REST
│   │   ├── models/        # Modelos de dados
│   │   ├── workers/       # Processadores de eventos
│   │   ├── services/      # Serviços de negócio
│   │   └── schemas/       # Schemas de validação
│   └── tests/             # Testes automatizados
├── frontend/
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── pages/         # Páginas da aplicação
│   │   └── services/      # Serviços de API
│   └── public/            # Arquivos estáticos
└── docker/                # Configurações Docker
```

## 🛠️ Tecnologias

### Backend
- **Python 3.9+**: Linguagem principal
- **FastAPI 0.68.1**: Framework web moderno e rápido
- **SQLAlchemy 1.4.23**: ORM para banco de dados
- **PostgreSQL**: Banco de dados relacional
- **RabbitMQ**: Message broker para processamento assíncrono
- **Pandas 1.3.3 & NumPy 1.21.2**: Processamento de dados
- **Scikit-learn 0.24.2**: Machine learning
- **Pydantic 1.8.2**: Validação de dados
- **Uvicorn 0.15.0**: Servidor ASGI
- **Python-dotenv 0.19.0**: Gerenciamento de variáveis de ambiente
- **Python-jose 3.3.0 & Passlib 1.7.4**: Autenticação e segurança
- **Psycopg2-binary 2.9.3**: Driver PostgreSQL

### Frontend
- **React**: Biblioteca UI
- **TypeScript**: Tipagem estática
- **Material-UI**: Componentes de interface
- **Redux**: Gerenciamento de estado
- **Axios**: Cliente HTTP
- **Chart.js**: Visualização de dados

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
# Edite o arquivo .env com suas configurações
```

3. Inicie os containers:
```bash
docker-compose up -d
```

4. Acesse a aplicação:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- RabbitMQ Management: http://localhost:15672
- PostgreSQL: localhost:5432

## ⚙️ Configuração

### Variáveis de Ambiente

```env
# Backend
DATABASE_URL=postgresql://user:password@db:5432/iagym
RABBITMQ_URL=amqp://guest:guest@rabbitmq:5672/
SECRET_KEY=your-secret-key
ENVIRONMENT=development

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

## 📖 Uso

### API Endpoints

#### Alunos
- `GET /aluno/`: Lista todos os alunos
- `POST /aluno/`: Cadastra novo aluno
- `GET /aluno/{aluno_id}`: Detalhes do aluno
- `PUT /aluno/{aluno_id}`: Atualiza aluno
- `DELETE /aluno/{aluno_id}`: Remove aluno
- `GET /aluno/{aluno_id}/frequencia`: Histórico de frequência
- `GET /aluno/{aluno_id}/risco-churn`: Análise de risco de churn

#### Check-ins
- `POST /aluno/checkin/`: Registra check-in
- `GET /aluno/checkin/aluno/{id}`: Histórico de check-ins
- `POST /aluno/checkin/batch`: Processa lote de check-ins

#### Planos
- `GET /plano/`: Lista todos os planos
- `POST /plano/`: Cadastra novo plano
- `GET /plano/{plano_id}`: Detalhes do plano
- `POST /plano/inicializar`: Inicializa planos padrão

### Documentação da API

A API é documentada usando o Swagger UI e ReDoc:

- **Swagger UI**: http://localhost:8000/docs
  - Interface interativa para testar os endpoints
  - Visualização detalhada dos modelos de dados
  - Exemplos de requisições e respostas

- **ReDoc**: http://localhost:8000/redoc
  - Documentação mais legível e organizada
  - Visualização em formato de página única

### Processamento de Eventos

O sistema utiliza RabbitMQ para processamento assíncrono de eventos:

1. **Check-ins em Lote**:
   - Fila: `checkins`
   - Routing Key: `gym.checkins.batch`

2. **Relatórios Diários**:
   - Fila: `daily_reports`
   - Routing Key: `gym.reports.daily`

3. **Análise de Churn**:
   - Fila: `churn_analysis`
   - Routing Key: `gym.churn.analyze`

## 🤝 Contribuição

1. Fork o projeto
2. Crie sua Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE.md](LICENSE.md) para detalhes.
