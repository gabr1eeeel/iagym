from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models, schemas
from app.database import get_db

router = APIRouter()

@router.post("/inicializar")
def inicializar_planos(db: Session = Depends(get_db)):
    # Verifica se já existem planos
    if db.query(models.Plano).count() > 0:
        return {"message": "Planos já inicializados"}

    # Cria planos iniciais
    planos_iniciais = [
        {"nome": "Básico", "preco": 99.90, "descricao": "Acesso à academia em horário comercial"},
        {"nome": "Premium", "preco": 199.90, "descricao": "Acesso ilimitado + aulas coletivas"},
        {"nome": "VIP", "preco": 299.90, "descricao": "Acesso ilimitado + personal trainer"}
    ]

    for plano in planos_iniciais:
        db_plano = models.Plano(**plano)
        db.add(db_plano)

    db.commit()
    return {"message": "Planos inicializados com sucesso"}

@router.get("/", response_model=List[schemas.Plano])
def listar_planos(db: Session = Depends(get_db)):
    planos = db.query(models.Plano).all()
    return planos

@router.post("/", response_model=schemas.Plano)
def criar_plano(plano: schemas.PlanoCreate, db: Session = Depends(get_db)):
    db_plano = models.Plano(**plano.dict())
    db.add(db_plano)
    db.commit()
    db.refresh(db_plano)
    return db_plano

@router.get("/{plano_id}", response_model=schemas.Plano)
def obter_plano(plano_id: int, db: Session = Depends(get_db)):
    plano = db.query(models.Plano).filter(models.Plano.id == plano_id).first()
    if not plano:
        raise HTTPException(status_code=404, detail="Plano não encontrado")
    return plano 