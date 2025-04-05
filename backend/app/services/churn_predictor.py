from datetime import datetime, timedelta
from app.models import Aluno, Checkin
from sqlalchemy.orm import Session

class ChurnPredictor:
    def __init__(self):
        self.pesos = {
            'frequencia': 0.4,
            'tempo_matricula': 0.3,
            'valor_plano': 0.3
        }

    def predict(self, aluno: Aluno) -> float:
        """Calcula o risco de churn do aluno"""
        risco = 0.0
        fatores = []

        # Fator 1: Frequência de check-ins
        frequencia = self._calcular_frequencia(aluno)
        if frequencia < 0.5:
            risco += self.pesos['frequencia'] * (1 - frequencia)
            fatores.append("Baixa frequência de check-ins")

        # Fator 2: Tempo de matrícula
        tempo_matricula = self._calcular_tempo_matricula(aluno)
        if tempo_matricula < 30:  # Menos de 30 dias
            risco += self.pesos['tempo_matricula'] * 0.7
            fatores.append("Tempo de matrícula recente")

        # Fator 3: Valor do plano
        if aluno.plano.preco > 199.90:  # Plano Premium ou VIP
            risco += self.pesos['valor_plano'] * 0.5
            fatores.append("Plano com valor elevado")

        return min(risco, 1.0)  # Garante que o risco não ultrapasse 1.0

    def get_fatores_risco(self, aluno: Aluno) -> list:
        """Retorna os fatores de risco identificados"""
        fatores = []
        
        frequencia = self._calcular_frequencia(aluno)
        if frequencia < 0.5:
            fatores.append("Baixa frequência de check-ins")

        tempo_matricula = self._calcular_tempo_matricula(aluno)
        if tempo_matricula < 30:
            fatores.append("Tempo de matrícula recente")

        if aluno.plano.preco > 199.90:
            fatores.append("Plano com valor elevado")

        return fatores

    def _calcular_frequencia(self, aluno: Aluno) -> float:
        """Calcula a frequência de check-ins do aluno"""
        if not aluno.checkins:
            return 0.0

        total_dias = 30  # Considera os últimos 30 dias
        checkins_30_dias = sum(1 for c in aluno.checkins 
                             if (datetime.utcnow() - c.data).days <= 30)
        
        return checkins_30_dias / total_dias

    def _calcular_tempo_matricula(self, aluno: Aluno) -> int:
        """Calcula o tempo de matrícula em dias"""
        return (datetime.utcnow() - aluno.data_matricula).days 