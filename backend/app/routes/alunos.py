from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timedelta
from app import models, schemas
from app.database import get_db
from app.services.churn_predictor import ChurnPredictor
from app.models.aluno import StatusMatricula

router = APIRouter()
churn_predictor = ChurnPredictor()

@router.get("/", response_model=List[schemas.Aluno])
def listar_alunos(db: Session = Depends(get_db)):
    alunos = db.query(models.Aluno).all()
    return alunos

def treinar_modelo(db: Session):
    """Função auxiliar para treinar o modelo"""
    try:
        # Obtém todos os alunos com seus dados
        alunos = db.query(models.Aluno).options(
            joinedload(models.Aluno.checkins),
            joinedload(models.Aluno.plano)
        ).all()
        
        if len(alunos) < 2:
            print("Dados insuficientes para treinar")
            return False
            
        # Prepara dados para treinamento
        X = []
        y = []
        
        for aluno in alunos:
            try:
                features = churn_predictor._extract_features(aluno)
                X.append(features[0])
                y.append(1 if aluno.status_matricula == StatusMatricula.CANCELADA.value else 0)
            except Exception as e:
                print(f"Erro ao processar aluno {aluno.id}: {e}")
                continue
        
        if len(X) > 0 and len(set(y)) > 1:
            print(f"Treinando modelo com {len(X)} amostras ({sum(y)} churns)")
            if churn_predictor.train(X, y):
                # Atualiza previsões para alunos ativos
                alunos_ativos = [a for a in alunos if a.status_matricula == StatusMatricula.ATIVA.value]
                for aluno_ativo in alunos_ativos:
                    try:
                        aluno_ativo.risco_churn = churn_predictor.predict(aluno_ativo)
                    except Exception as e:
                        print(f"Erro ao atualizar risco do aluno {aluno_ativo.id}: {e}")
                db.commit()
                return True
        return False
    except Exception as e:
        print(f"Erro ao treinar modelo: {e}")
        return False

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

    # Treina o modelo se necessário (isso já atualiza o risco de todos os alunos)
    treinar_modelo(db)
    
    # Recarrega o aluno para pegar o risco atualizado
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
    aluno = db.query(models.Aluno).options(
        joinedload(models.Aluno.checkins),
        joinedload(models.Aluno.plano)
    ).filter(models.Aluno.id == aluno_id).first()
    
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Calcula e atualiza o risco
    risco = churn_predictor.predict(aluno)
    aluno.risco_churn = risco
    db.commit()
    
    # Obtém os fatores de risco
    fatores = churn_predictor.get_fatores_risco(aluno)

    return {
        "risco": risco,
        "fatores": fatores
    }

@router.post("/{aluno_id}/checkin", response_model=schemas.Checkin)
def registrar_checkin(aluno_id: int, db: Session = Depends(get_db)):
    # Verifica se o aluno existe
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Cria o check-in
    db_checkin = models.Checkin(
        aluno_id=aluno_id,
        data=datetime.utcnow()
    )
    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)

    # Treina o modelo periodicamente (isso já atualiza o risco de todos os alunos)
    if db_checkin.id % 10 == 0:  # A cada 10 checkins
        treinar_modelo(db)
    else:
        # Se não treinou o modelo, atualiza só o risco deste aluno
        aluno.risco_churn = churn_predictor.predict(aluno)
        db.commit()
    
    return db_checkin

@router.post("/{aluno_id}/cancelar", response_model=schemas.Aluno)
def cancelar_matricula(aluno_id: int, db: Session = Depends(get_db)):
    # Verifica se o aluno existe
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
        
    if aluno.status_matricula == StatusMatricula.CANCELADA.value:
        raise HTTPException(status_code=400, detail="Matrícula já está cancelada")

    # Atualiza o status da matrícula
    aluno.status_matricula = StatusMatricula.CANCELADA.value
    aluno.data_cancelamento = datetime.utcnow()
    db.commit()
    db.refresh(aluno)

    # Treina o modelo com os novos dados (isso já atualiza o risco de todos os alunos)
    treinar_modelo(db)
    
    # Recarrega o aluno para pegar o risco atualizado
    db.refresh(aluno)
    return aluno

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

    # Atualiza a data de cancelamento se o status mudou para CANCELADA
    if (aluno.status_matricula == StatusMatricula.CANCELADA.value and 
        db_aluno.status_matricula != StatusMatricula.CANCELADA.value):
        db_aluno.data_cancelamento = datetime.utcnow()
    elif (aluno.status_matricula == StatusMatricula.ATIVA.value and 
          db_aluno.status_matricula != StatusMatricula.ATIVA.value):
        db_aluno.data_cancelamento = None

    # Atualiza os campos do aluno
    for key, value in aluno.dict(exclude_unset=True).items():
        setattr(db_aluno, key, value)

    db.commit()
    db.refresh(db_aluno)

    # Atualiza o risco de churn
    db_aluno.risco_churn = churn_predictor.predict(db_aluno)
    db.commit()
    db.refresh(db_aluno)

    return db_aluno

@router.delete("/{aluno_id}")
def deletar_aluno(aluno_id: int, db: Session = Depends(get_db)):
    # Verifica se o aluno existe
    aluno = db.query(models.Aluno).filter(models.Aluno.id == aluno_id).first()
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")

    # Remove o aluno
    db.delete(aluno)
    db.commit()

    return {"message": "Aluno deletado com sucesso"} 