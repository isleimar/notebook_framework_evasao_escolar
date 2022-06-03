from scripts.selecao import Selecao
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFE

class SelecaoWrapper(Selecao):
    def __init__(self, arq, alvo):
        super().__init__(arq, alvo)
        
    def selecionarFeatures(self):
        x = self.campos
        y = self.alvo
        modelo = LogisticRegression(max_iter=1000)
        rfe = RFE(modelo, n_features_to_select=self.qtdCampos, step=1)
        fitrfe = rfe.fit(x,y.values.ravel())
        cols = fitrfe.get_support(indices=True)
        return list(x.iloc[:,cols].columns)
    