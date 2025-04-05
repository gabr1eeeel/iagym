from datetime import datetime, timedelta
import numpy as np
import joblib
import os
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from app.models import Aluno, Checkin
from sqlalchemy.orm import Session

class ChurnPredictor:
    def __init__(self):
        """
        Inicializa o preditor de churn com um RandomForestClassifier
        e um StandardScaler para normalização dos dados
        """
        self.model_dir = Path("app/ml_models")
        self.model_path = self.model_dir / "churn_model.joblib"
        self.scaler_path = self.model_dir / "scaler.joblib"
        
        # Cria diretório se não existir
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        # Inicializa o modelo
        self._initialize_model()

    def _initialize_model(self):
        """Inicializa ou carrega o modelo existente"""
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            class_weight='balanced',  # Importante para dados desbalanceados
            random_state=42
        )
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Tenta carregar modelo existente
        try:
            if self.model_path.exists() and self.scaler_path.exists():
                self.model = joblib.load(self.model_path)
                self.scaler = joblib.load(self.scaler_path)
                self.is_trained = True
                print("Modelo de churn carregado com sucesso")
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            print("Usando modelo inicial")

    def _extract_features(self, aluno: Aluno) -> np.ndarray:
        """
        Extrai as features do aluno para predição
        
        Args:
            aluno: Objeto do aluno com seus dados e checkins
            
        Returns:
            np.ndarray: Array com as features normalizadas
        """
        hoje = datetime.utcnow()
        
        # Validação inicial
        if not aluno:
            raise ValueError("Aluno não pode ser nulo")
        if not hasattr(aluno, 'checkins'):
            raise ValueError("Aluno não tem checkins carregados")
        if not hasattr(aluno, 'plano'):
            raise ValueError("Aluno não tem plano carregado")
            
        # 1. Features de frequência
        checkins_validos = [c for c in aluno.checkins if c.data and c.data <= hoje]
        
        # Frequência última semana
        checkins_semana = sum(1 for c in checkins_validos 
                            if (hoje - c.data).days <= 7)
        freq_semanal = min(checkins_semana / 7.0, 1.0)  # Limita a 100%
        
        # Frequência último mês
        checkins_mes = sum(1 for c in checkins_validos 
                          if (hoje - c.data).days <= 30)
        freq_mensal = min(checkins_mes / 30.0, 1.0)  # Limita a 100%
        
        # 2. Features temporais
        # Dias desde último checkin
        if checkins_validos:
            datas_checkin = [c.data for c in checkins_validos]
            ultimo_checkin = max(datas_checkin)
            dias_ultimo_checkin = min((hoje - ultimo_checkin).days, 365)  # Limita a 1 ano
            
            # Variância entre checkins (regularidade)
            if len(datas_checkin) > 1:
                datas_ordenadas = sorted(datas_checkin)
                intervalos = [(datas_ordenadas[i+1] - datas_ordenadas[i]).days 
                            for i in range(len(datas_ordenadas)-1)]
                variancia_intervalos = float(np.clip(np.var(intervalos), 0, 100)) if intervalos else 30
            else:
                variancia_intervalos = 30
        else:
            dias_ultimo_checkin = 365  # Se nunca fez checkin, assume 1 ano
            variancia_intervalos = 30
            
        # 3. Features de engajamento
        if not aluno.data_matricula:
            raise ValueError("Aluno não tem data de matrícula")
            
        tempo_matricula = max((hoje - aluno.data_matricula).days, 1)  # Evita divisão por zero
        total_checkins = len(checkins_validos)
        media_checkins_vida = min(total_checkins / tempo_matricula, 1.0)  # Limita a 1 por dia
        
        # 4. Features do plano
        preco_plano = float(aluno.plano.preco) if aluno.plano and aluno.plano.preco else 0.0
            
        features = np.array([[
            freq_semanal,
            freq_mensal,
            dias_ultimo_checkin,
            variancia_intervalos,
            tempo_matricula,
            media_checkins_vida,
            preco_plano
        ]])
        
        if self.is_trained:
            try:
                features = self.scaler.transform(features)
            except Exception as e:
                print(f"Erro ao normalizar features: {e}")
                # Se falhar a normalização, usa os valores não normalizados
                pass
        
        return features

    def predict(self, aluno: Aluno) -> float:
        """Prediz a probabilidade de churn do aluno"""
        try:
            features = self._extract_features(aluno)
            
            if not self.is_trained:
                return self._heuristic_prediction(features)
            
            # Usa o modelo treinado
            try:
                probas = self.model.predict_proba(features)
                if probas.shape[1] < 2:
                    print("Modelo não tem duas classes, usando heurística")
                    return self._heuristic_prediction(features)
                
                prob_churn = float(probas[0][1])
                print(f"Probabilidade de churn para aluno {aluno.id}: {prob_churn}")
                return prob_churn
                
            except Exception as e:
                print(f"Erro na predição do modelo: {e}")
                return self._heuristic_prediction(features)
                
        except Exception as e:
            print(f"Erro ao predizer churn: {e}")
            return 0.5  # Valor neutro em caso de erro
    
    def _heuristic_prediction(self, features) -> float:
        """Calcula predição baseada em heurística quando não há modelo treinado"""
        freq_semanal = features[0][0]  # 0 a 1
        freq_mensal = features[0][1]   # 0 a 1
        dias_sem_checkin = features[0][2]  # 0 a 365
        tempo_matricula = features[0][4]   # em dias
        media_checkins_vida = features[0][5]  # 0 a 1
        
        score = 0.0
        
        # Frequência alta reduz o risco
        if freq_semanal >= 0.5:  # Mais de 3-4 vezes por semana
            score -= 0.3
        elif freq_semanal < 0.15:  # Menos de 1 vez por semana
            score += 0.4
            
        # Inatividade recente é um forte indicador de risco
        if dias_sem_checkin > 14:  # Mais de duas semanas sem checkin
            score += 0.5
        elif dias_sem_checkin <= 3:  # Checkin recente
            score -= 0.2
            
        # Frequência mensal consistente reduz risco
        if freq_mensal >= 0.4:  # Mais de 12 vezes por mês
            score -= 0.2
        elif freq_mensal < 0.15:  # Menos de 5 vezes por mês
            score += 0.3
            
        # Engajamento ao longo do tempo
        if media_checkins_vida >= 0.4:  # Média alta de checkins
            score -= 0.2
        elif media_checkins_vida < 0.1:  # Média muito baixa
            score += 0.2
            
        # Ajuste baseado no tempo de matrícula
        if tempo_matricula < 30:  # Primeiro mês é crítico
            if score > 0:  # Se já tem sinais de risco
                score *= 1.2
            else:  # Se está indo bem, reduz o peso do período inicial
                score *= 0.8
        
        # Normaliza o score entre 0 e 1
        return max(min(score + 0.5, 1.0), 0.0)  # Centraliza em 0.5 e limita entre 0 e 1

    def get_fatores_risco(self, aluno: Aluno) -> list:
        """Retorna os fatores de risco identificados para o aluno"""
        features = self._extract_features(aluno)
        if self.is_trained:
            features = self.scaler.inverse_transform(features)
            
        freq_semanal = features[0][0]
        freq_mensal = features[0][1]
        dias_sem_checkin = features[0][2]
        variancia_intervalos = features[0][3]
        tempo_matricula = features[0][4]
        media_checkins_vida = features[0][5]
        
        fatores = []
        
        # Análise de frequência (ajustada para ser mais precisa)
        if freq_semanal < 0.15:
            fatores.append("Frequência muito baixa (menos de 1 vez por semana)")
        elif freq_semanal < 0.3:
            fatores.append("Frequência baixa (menos de 2 vezes por semana)")
            
        # Análise de inatividade (mais granular)
        if dias_sem_checkin > 14:
            fatores.append(f"Inativo há {int(dias_sem_checkin)} dias - Risco Alto")
        elif dias_sem_checkin > 7 and tempo_matricula > 7:
            fatores.append(f"Inativo há {int(dias_sem_checkin)} dias - Atenção")
            
        # Análise de regularidade (ajustada para ser mais precisa)
        if variancia_intervalos > 20 and tempo_matricula > 30:
            fatores.append("Frequência muito irregular")
        elif variancia_intervalos > 10 and tempo_matricula > 30:
            fatores.append("Frequência pouco regular")
            
        # Análise de engajamento geral
        if tempo_matricula > 30:
            if media_checkins_vida < 0.1:
                fatores.append("Histórico de engajamento muito baixo")
            elif media_checkins_vida < 0.2:
                fatores.append("Histórico de engajamento abaixo do esperado")
                
        # Avaliação do período inicial
        if tempo_matricula <= 30 and freq_semanal < 0.3:
            fatores.append("Baixo engajamento no início da matrícula - Atenção Especial")
            
        return fatores

    def save_model(self):
        """Salva o modelo e o scaler em disco"""
        if self.is_trained:
            try:
                joblib.dump(self.model, self.model_path)
                joblib.dump(self.scaler, self.scaler_path)
                print("Modelo salvo com sucesso")
            except Exception as e:
                print(f"Erro ao salvar modelo: {e}")

    def train(self, X, y):
        """Treina o modelo com os dados fornecidos"""
        try:
            if len(X) < 2 or len(set(y)) < 2:
                print("Dados insuficientes para treinar o modelo")
                return False
                
            X = np.array(X)
            y = np.array(y)
            
            # Normaliza os dados
            self.scaler.fit(X)
            X_scaled = self.scaler.transform(X)
            
            # Configura o modelo para dar mais peso à classe minoritária
            n_samples = len(y)
            n_churns = sum(y)
            if n_churns > 0:
                class_weight = {
                    0: 1.0,
                    1: (n_samples - n_churns) / n_churns  # Balanceia as classes
                }
                self.model.set_params(class_weight=class_weight)
            
            # Treina o modelo
            self.model.fit(X_scaled, y)
            self.is_trained = True
            
            # Salva o modelo
            self.save_model()
            
            print(f"Modelo treinado com sucesso: {len(X)} amostras, {sum(y)} churns")
            return True
            
        except Exception as e:
            print(f"Erro ao treinar modelo: {e}")
            return False 