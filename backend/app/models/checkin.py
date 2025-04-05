from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Checkin(Base):
    __tablename__ = "checkins"

    id = Column(Integer, primary_key=True, index=True)
    aluno_id = Column(Integer, ForeignKey("alunos.id"))
    data = Column(DateTime, default=datetime.utcnow)

    # Relacionamentos
    aluno = relationship("Aluno", back_populates="checkins")

    def __repr__(self):
        return f"<Checkin {self.id}>" 