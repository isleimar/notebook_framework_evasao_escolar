import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE

class Selecao:
    def __init__(self, arq, alvo):
        self.__nomeArq = arq
        self.__nomeAlvo = alvo        
        self.__nomeCampos = []
        self.__selecionados = []
        self.__df = None
        self.__alvo = None
        self.__campos = None
        self.__balanceada = False
        self.__qtdCampos = None;
        pd.set_option('mode.chained_assignment',None)
    
    def selecionarFeatures(self): pass
        
    def __filtrarCampos(self, df):
        self.__nomeCampos = list(filter(lambda a: a != self.nomeAlvo, list(df)))
        self.__campos = df[self.__nomeCampos]
        if self.__qtdCampos is None:
            self.__qtdCampos = len(self.__campos)
        
    def __converterEmNumericas(self):
        le = LabelEncoder()
        for nome in self.__nomeCampos:
            self.__campos[nome] = le.fit_transform(self.__campos[nome])        
    
    def __dimensionando(self):
        mi_ma = MinMaxScaler()
        for nome in self.__nomeCampos:
            self.__campos[[nome]] = mi_ma.fit_transform(self.__campos[[nome]])
    
    def __balancear(self):
        oversample = SMOTE(random_state=42)
        self.__campos, self.__alvo = oversample.fit_resample(self.campos, self.alvo)
        
    @property
    def nomeArq(self)->str:
        return self.__nomeArq
    
    @property
    def nomeAlvo(self)->str:
        return self.__nomeAlvo
    
    @property
    def nomeCampos(self)->str:
        return self.__nomeCampos
    
    @property
    def campos(self):
        return self.__campos
    
    @property
    def alvo(self):
        return self.__alvo
    
    @property
    def balanceada(self)->bool:
        return self.__balanceada
    @balanceada.setter
    def balanceada(self, balanceada):
        self.__balanceada = balanceada
    
    @property
    def selecionados(self):
        return self.__selecionados
    
    @property
    def qtdCampos(self):
        return self.__qtdCampos
    @qtdCampos.setter
    def qtdCampos(self,qtdCampos):
        self.__qtdCampos = qtdCampos
        
    def iniciar(self):
        df = pd.read_csv(self.__nomeArq)
        self.__alvo = df[[self.__nomeAlvo]]
        self.__filtrarCampos(df)
        self.__converterEmNumericas()
        self.__dimensionando()
        if self.balanceada:
            self.__balancear()
        self.__selecionados = self.selecionarFeatures()
    
    
        
    
    
        