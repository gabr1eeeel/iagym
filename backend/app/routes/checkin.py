from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from app import models, schemas
from app.database import get_db
from app.services.churn_predictor import ChurnPredictor

router = APIRouter()
churn_predictor = ChurnPredictor()

@router.post("/", response_model=schemas.Checkin)
def registrar_checkin(checkin: schemas.CheckinCreate, db: Session = Depends(get_db)):
    # Verifica se o aluno existe
    aluno = db.query(models.Aluno).filter(models.Aluno.id == checkin.aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Cria o check-in
    db_checkin = models.Checkin(**checkin.dict(), data=datetime.utcnow())
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)

    # Atualiza o risco de churn
    risco_churn = churn_predictor.predict(aluno)
    aluno.risco_churn = risco_churn
    db.commit()
    db.refresh(aluno)

    return db_checkin 