from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import alunos, planos, checkin
from app.database import engine, Base

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IA Gym API")

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(alunos.router, prefix="/aluno", tags=["alunos"])
app.include_router(planos.router, prefix="/plano", tags=["planos"])
app.include_router(checkin.router, prefix="/aluno/checkin", tags=["checkin"])

@app.get("/")
def root():
    return {"message": "Bem-vindo à API do IA Gym"} 