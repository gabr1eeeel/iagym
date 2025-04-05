from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Plano(Base):
    __tablename__ = "planos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, unique=True, index=True)
    preco = Column(Float)
    descricao = Column(String)

    # Relacionamentos
    alunos = relationship("Aluno", back_populates="plano")

    def __repr__(self):
        return f"<Plano {self.nome}>" 