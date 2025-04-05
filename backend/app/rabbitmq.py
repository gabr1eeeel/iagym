import pika
import json
import os
from typing import Any, Dict, List
from functools import wraps
from datetime import datetime
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.url = os.getenv('RABBITMQ_URL')
        if not self.url:
            raise ValueError("RABBITMQ_URL não configurada no arquivo .env")

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(
                pika.URLParameters(self.url)
            )
            self.channel = self.connection.channel()
            
            # Declarar exchanges
            self.channel.exchange_declare(
                exchange='gym_events',
                exchange_type='topic',
                durable=True
            )
            
            # Declarar filas
            queues = {
                'checkins': 'gym.checkins.*',
                'daily_reports': 'gym.reports.daily',
                'churn_analysis': 'gym.churn.*',
                'batch_processing': 'gym.batch.*'
            }
            
            for queue, routing_pattern in queues.items():
                self.channel.queue_declare(queue=queue, durable=True)
                self.channel.queue_bind(
                    exchange='gym_events',
                    queue=queue,
                    routing_key=routing_pattern
                )

    def publish_message(self, routing_key: str, message: Dict[str, Any]):
        try:
            if not self.connection or self.connection.is_closed:
                self.connect()
                
            self.channel.basic_publish(
                exchange='gym_events',
                routing_key=routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # Mensagem persistente
                    content_type='application/json'
                )
            )
        except Exception as e:
            print(f"Erro ao publicar mensagem: {str(e)}")
            raise

    def publish_batch_checkins(self, checkins: List[Dict[str, Any]]):
        """Publica um lote de checkins para processamento"""
        self.publish_message(
            routing_key='gym.checkins.batch',
            message={'checkins': checkins}
        )

    def schedule_daily_report(self, data_referencia: str):
        """Agenda geração de relatório diário"""
        self.publish_message(
            routing_key='gym.reports.daily',
            message={'data_referencia': data_referencia}
        )

    def trigger_churn_analysis(self):
        """Dispara análise de churn para todos os alunos"""
        self.publish_message(
            routing_key='gym.churn.analyze',
            message={'tipo': 'analise_completa', 'data': datetime.utcnow().isoformat()}
        )

    def consume(self, queue: str, callback: callable):
        def wrapper(ch, method, properties, body):
            message = json.loads(body)
            callback(message)

        self.channel.basic_consume(
            queue=queue,
            on_message_callback=wrapper,
            auto_ack=True
        )

        self.channel.start_consuming()

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

rabbitmq_client = RabbitMQClient()

def ensure_connection(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not rabbitmq_client.connection or rabbitmq_client.connection.is_closed:
            rabbitmq_client.connect()
        return func(*args, **kwargs)
    return wrapper 