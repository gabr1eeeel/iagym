from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class PlanoBase(BaseModel):
    nome: str
    preco: float
    descricao: str

class PlanoCreate(PlanoBase):
    pass

class Plano(PlanoBase):
    id: int

    class Config:
        orm_mode = True

class AlunoBase(BaseModel):
    nome: str
    email: str
    telefone: str
    plano_id: int

class AlunoCreate(AlunoBase):
    pass

class Aluno(AlunoBase):
    id: int
    data_matricula: datetime
    nome_plano: str
    risco_churn: float

    class Config:
        orm_mode = True

class AlunoUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    telefone: Optional[str] = None
    plano_id: Optional[int] = None
    nome_plano: Optional[str] = None

    class Config:
        orm_mode = True

class CheckinBase(BaseModel):
    aluno_id: int

class CheckinCreate(CheckinBase):
    pass

class Checkin(CheckinBase):
    id: int
    data: datetime

    class Config:
        orm_mode = True

class Frequencia(BaseModel):
    total_dias: int
    dias_presentes: int
    percentual: float

class RiscoChurn(BaseModel):
    risco: float
    fatores: List[str] 