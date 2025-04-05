from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Aluno(Base):
    __tablename__ = "alunos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    telefone = Column(String)
    plano_id = Column(Integer, ForeignKey("planos.id"))
    data_matricula = Column(DateTime, default=datetime.utcnow)
    nome_plano = Column(String)
    risco_churn = Column(Float, default=0.0)

    # Relacionamentos
    plano = relationship("Plano", back_populates="alunos")
    checkins = relationship("Checkin", back_populates="aluno")

    def __repr__(self):
        return f"<Aluno {self.nome}>" 