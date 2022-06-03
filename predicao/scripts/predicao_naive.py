from scripts.predicao import Predicao
from sklearn.naive_bayes import ComplementNB 

class PredicaoNaive(Predicao):    
    def __init__(self, arq, alvo):
        super().__init__(arq, alvo)
    
    def classeClassificador(self):
        return ComplementNB(random_state=42)
        
    
    