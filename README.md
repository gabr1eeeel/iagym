# IA Gym - Sistema de Monitoramento de Academia

Sistema para monitorar a frequência dos alunos e prever possíveis desistências (churn) em academias.

## Requisitos

- Docker
- Docker Compose

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/iagym.git
cd iagym
```

2. Inicie os serviços usando Docker Compose:
```bash
docker-compose up -d
```

A API estará disponível em `http://localhost:8000`

## Documentação da API

A documentação interativa da API está disponível em:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints Principais

### Alunos
- `POST /aluno/registro`: Registrar um novo aluno
- `POST /aluno/checkin`: Registrar entrada do aluno na academia
- `GET /aluno/{id}/frequencia`: Obter histórico de frequência
- `GET /aluno/{id}/risco-churn`: Obter probabilidade de desistência

## Estrutura do Projeto

```
iagym/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── init_db.py
│   └── routers/
│       └── alunos.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Desenvolvimento

Para desenvolvimento local:

1. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Execute a aplicação:
```bash
uvicorn app.main:app --reload
```

## Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request
