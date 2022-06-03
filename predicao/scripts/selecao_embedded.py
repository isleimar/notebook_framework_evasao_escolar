from scripts.selecao import Selecao
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

class SelecaoEmbedded(Selecao):
    def __init__(self, arq, alvo):
        super().__init__(arq, alvo)
        self.__importcancia = None
    
    @property
    def importancia(self):
        return self.__importcancia
        
    def selecionarFeatures(self):
        x = self.campos
        y = self.alvo
        modelo = RandomForestClassifier(n_estimators=self.qtdCampos)
        modelo.fit(x,y.values.ravel())
        self.__importcancia = pd.DataFrame(
            modelo.feature_importances_,
            index = x.columns,
            columns=['importancia']).sort_values('importancia', ascending = False)
        return list(self.__importcancia.index)[:self.qtdCampos]
    