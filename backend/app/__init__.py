from app.models import aluno, plano, checkin
from app.schemas import Aluno, AlunoCreate, Plano, PlanoCreate, Checkin, CheckinCreate, Frequencia, RiscoChurn
from app.services import churn_predictor 