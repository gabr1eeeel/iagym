import pika
import json
import os
import sys
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Adicionar o diretório raiz ao PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from app.models import Aluno, Checkin, Plano
from app.database import SessionLocal
from app.ml.churn_predictor import churn_predictor

def process_checkin_batch(ch, method, properties, body):
    """
    Processa um lote de checkins recebidos via RabbitMQ
    """
    try:
        data = json.loads(body)
        checkins = data.get('checkins', [])
        
        if not checkins:
            print("Nenhum checkin recebido para processamento")
            return
        
        session = SessionLocal()
        
        for checkin_data in checkins:
            aluno_id = checkin_data.get('aluno_id')
            data_checkin = datetime.fromisoformat(checkin_data.get('data'))
            
            # Verifica se o aluno existe
            aluno = session.query(Aluno).filter(Aluno.id == aluno_id).first()
            if not aluno:
                print(f"Aluno com ID {aluno_id} não encontrado")
                continue
            
            # Cria o checkin
            novo_checkin = Checkin(
                aluno_id=aluno_id,
                data=data_checkin
            )
            
            session.add(novo_checkin)
        
        session.commit()
        print(f"Processados {len(checkins)} checkins com sucesso")
        
    except Exception as e:
        print(f"Erro ao processar lote de checkins: {str(e)}")
    finally:
        session.close()

def process_daily_report(ch, method, properties, body):
    """
    Gera relatório diário de frequência dos alunos
    """
    try:
        data = json.loads(body)
        data_referencia = datetime.fromisoformat(data.get('data_referencia'))
        
        # Define o período de análise (últimos 30 dias)
        data_inicio = data_referencia - timedelta(days=30)
        
        session = SessionLocal()
        
        # Consulta todos os alunos
        alunos = session.query(Aluno).all()
        
        relatorio = []
        
        for aluno in alunos:
            # Conta checkins no período
            total_checkins = session.query(func.count(Checkin.id)).filter(
                Checkin.aluno_id == aluno.id,
                Checkin.data >= data_inicio,
                Checkin.data <= data_referencia
            ).scalar()
            
            # Calcula frequência
            frequencia = total_checkins / 30.0  # 30 dias
            
            relatorio.append({
                'aluno_id': aluno.id,
                'nome': aluno.nome,
                'total_checkins': total_checkins,
                'frequencia': frequencia,
                'periodo': f"{data_inicio.date()} a {data_referencia.date()}"
            })
        
        # Salva o relatório (aqui você pode implementar a lógica para salvar em arquivo ou banco)
        print(f"Relatório diário gerado para {len(relatorio)} alunos")
        print(json.dumps(relatorio, indent=2, default=str))
        
    except Exception as e:
        print(f"Erro ao gerar relatório diário: {str(e)}")
    finally:
        session.close()

def process_churn_analysis(ch, method, properties, body):
    """
    Atualiza o modelo de previsão de churn para todos os alunos
    """
    try:
        data = json.loads(body)
        tipo_analise = data.get('tipo', 'analise_completa')
        
        session = SessionLocal()
        
        # Obtém todos os alunos
        alunos = session.query(Aluno).all()
        
        for aluno in alunos:
            # Obtém dados do aluno para previsão
            dados_aluno = {
                'aluno_id': aluno.id,
                'dias_matricula': (datetime.now() - aluno.data_matricula).days,
                'frequencia': session.query(func.count(Checkin.id)).filter(
                    Checkin.aluno_id == aluno.id,
                    Checkin.data >= datetime.now() - timedelta(days=30)
                ).scalar() / 30.0
            }
            
            # Faz a previsão de churn
            risco_churn = churn_predictor.predict(dados_aluno)
            
            # Atualiza o risco de churn do aluno
            aluno.risco_churn = risco_churn
            session.add(aluno)
        
        session.commit()
        print(f"Análise de churn concluída para {len(alunos)} alunos")
        
    except Exception as e:
        print(f"Erro ao realizar análise de churn: {str(e)}")
    finally:
        session.close()

def process_batch(ch, method, properties, body):
    """
    Processa operações em lote
    """
    try:
        data = json.loads(body)
        operacao = data.get('operacao')
        
        if operacao == 'checkins':
            process_checkin_batch(ch, method, properties, body)
        elif operacao == 'relatorio':
            process_daily_report(ch, method, properties, body)
        elif operacao == 'churn':
            process_churn_analysis(ch, method, properties, body)
        else:
            print(f"Operação em lote desconhecida: {operacao}")
            
    except Exception as e:
        print(f"Erro ao processar operação em lote: {str(e)}")

def main():
    url = os.getenv('RABBITMQ_URL')
    if not url:
        raise ValueError("RABBITMQ_URL não configurada no arquivo .env")
    
    connection = pika.BlockingConnection(pika.URLParameters(url))
    channel = connection.channel()
    
    # Configurar consumidores
    channel.basic_consume(queue='checkins', on_message_callback=process_checkin_batch)
    channel.basic_consume(queue='daily_reports', on_message_callback=process_daily_report)
    channel.basic_consume(queue='churn_analysis', on_message_callback=process_churn_analysis)
    channel.basic_consume(queue='batch_processing', on_message_callback=process_batch)
    
    print("Iniciando processamento de eventos. Para sair pressione CTRL+C")
    channel.start_consuming()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Encerrando worker...") 