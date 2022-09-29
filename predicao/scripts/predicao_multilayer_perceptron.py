from scripts.predicao import Predicao
from sklearn.neural_network import MLPClassifier


class PredicaoMultilayerPerceptron(Predicao):    
    def __init__(self, arq, alvo):
        super().__init__(arq, alvo)
    
    def classeClassificador(self):
        return MLPClassifier(random_state=42, max_iter=300)
        
    
    