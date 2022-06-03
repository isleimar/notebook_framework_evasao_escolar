from scripts.selecao import Selecao
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

class SelecaoChi2(Selecao):
    def __init__(self, arq, alvo):
        super().__init__(arq, alvo)
        
    def selecionarFeatures(self):
        x = self.campos
        y = self.alvo
        testechi = SelectKBest(chi2,k=self.qtdCampos)
        testechifeat = testechi.fit(x,y)        
        features = testechifeat.transform(x)
        cols = testechifeat.get_support(indices=True)
        return list(x.iloc[:,cols].columns)        
    