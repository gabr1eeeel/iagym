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