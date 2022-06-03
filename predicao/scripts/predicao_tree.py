from scripts.predicao import Predicao
from sklearn.tree import DecisionTreeClassifier


class PredicaoTree(Predicao):    
    def __init__(self, arq, alvo):
        super().__init__(arq, alvo)
    
    def getClassificador(self):
        return DecisionTreeClassifier(random_state=42)
        
    
    