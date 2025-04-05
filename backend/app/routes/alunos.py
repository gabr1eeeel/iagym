from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app import models, schemas
from app.database import get_db
from app.services.churn_predictor import ChurnPredictor

router = APIRouter()
churn_predictor = ChurnPredictor()

@router.get("/", response_model=List[schemas.Aluno])
def listar_alunos(db: Session = Depends(get_db)):
    alunos = db.query(models.Aluno).all()
    return alunos

@router.post("/", response_model=schemas.Aluno)
def criar_aluno(aluno: schemas.AlunoCreate, db: Session = Depends(get_db)):
    # Verifica se o email já existe
    aluno_existente = db.query(models.Aluno).filter(models.Aluno.email == aluno.email).first()
    if aluno_existente:
        raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Verifica se o plano existe
    plano = db.query(models.Plano).filter(models.Plano.id == aluno.plano_id).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")

    # Cria o aluno com o nome do plano
    db_aluno = models.Aluno(
        **aluno.dict(),
        nome_plano=plano.nome
    )
    db.add(db_aluno)
    db.commit()
    db.refresh(db_aluno)

    # Atualiza o risco de churn
    risco_churn = churn_predictor.predict(db_aluno)
    db_aluno.risco_churn = risco_churn
    db.commit()
    db.refresh(db_aluno)

    return db_aluno

@router.get("/{aluno_id}/frequencia", response_model=schemas.Frequencia)
def obter_frequencia(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Calcula a frequência dos últimos 30 dias
    data_inicio = datetime.utcnow() - timedelta(days=30)
    checkins = db.query(models.Checkin).filter(
        models.Checkin.aluno_id == aluno_id,
        models.Checkin.data >= data_inicio
    ).all()

    total_dias = 30
    dias_presentes = len(checkins)
    percentual = dias_presentes / total_dias

    return {
        "total_dias": total_dias,
        "dias_presentes": dias_presentes,
        "percentual": percentual
    }

@router.get("/{aluno_id}/risco-churn", response_model=schemas.RiscoChurn)
def obter_risco_churn(aluno_id: int, db: Session = Depends(get_db)):
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    risco = churn_predictor.predict(aluno)
    fatores = churn_predictor.get_fatores_risco(aluno)

    return {
        "risco": risco,
        "fatores": fatores
    }

@router.delete("/{aluno_id}")
def excluir_aluno(aluno_id: int, db: Session = Depends(get_db)):
    # Verifica se o aluno existe
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Exclui os checkins do aluno
    db.query(models.Checkin).filter(models.Checkin.aluno_id == aluno_id).delete()

    # Exclui o aluno
    db.delete(aluno)
    db.commit()

    return {"message": "Aluno excluído com sucesso"}

@router.put("/{aluno_id}", response_model=schemas.Aluno)
def atualizar_aluno(aluno_id: int, aluno: schemas.AlunoUpdate, db: Session = Depends(get_db)):
    # Verifica se o aluno existe
    db_aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not db_aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Verifica se o email já existe (se estiver sendo alterado)
    if aluno.email and aluno.email != db_aluno.email:
        aluno_existente = db.query(models.Aluno).filter(
            models.Aluno.email == aluno.email,
            models.Aluno.id != aluno_id
        ).first()
        if aluno_existente:
            raise HTTPException(status_code=400, detail="Email já cadastrado")

    # Verifica se o plano existe (se estiver sendo alterado)
    if aluno.plano_id:
        plano = db.query(models.Plano).filter(models.Plano.id == aluno.plano_id).first()
        if not plano:
            raise HTTPException(status_code=404, detail="Plano não encontrado")
        aluno.nome_plano = plano.nome

    # Atualiza os campos do aluno
    for key, value in aluno.dict(exclude_unset=True).items():
        setattr(db_aluno, key, value)

    db.commit()
    db.refresh(db_aluno)

    # Atualiza o risco de churn
    risco_churn = churn_predictor.predict(db_aluno)
    db_aluno.risco_churn = risco_churn
    db.commit()
    db.refresh(db_aluno)

    return db_aluno 