from scripts.predicao import Predicao
from sklearn.ensemble import RandomForestClassifier


class PredicaoRandomForest(Predicao):    
    def __init__(self, arq, alvo):
        super().__init__(arq, alvo)
    
    def classeClassificador(self):
        return RandomForestClassifier(n_estimators=20, random_state=42)
        
    
    