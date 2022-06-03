from scripts.selecao import Selecao
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import f_classif

class SelecaoKBest(Selecao):
    def __init__(self, arq, alvo):
        super().__init__(arq, alvo)
        
    def selecionarFeatures(self):
        x = self.campos
        y = self.alvo
        f_classiftest = SelectKBest(score_func=f_classif,k=self.qtdCampos)
        modelofeat = f_classiftest.fit(x,y.values.ravel())
        features = modelofeat.transform(x)
        cols = modelofeat.get_support(indices=True)
        return list(x.iloc[:,cols].columns)        
    