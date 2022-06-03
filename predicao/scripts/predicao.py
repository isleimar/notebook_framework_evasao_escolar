import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import mean_squared_error
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score

class Predicao:
    
    def __init__(self, df, alvo):
        self.__df = df
        self.__nomeAlvo = alvo
        self.__nomeCampos = []
        self.__metricas = ['accuracy','precision','recall','roc_auc','f1']
        self.__campos = None
        self.__alvo = None
        self.__balanceada = False
        self.__holdout ={
            'accuracy': accuracy_score,
            'precision': precision_score,
            'recall': recall_score,
            'roc_auc': roc_auc_score,
            'f1': f1_score,            
        }
        self.__x_treino = None
        self.__x_teste = None
        self.__y_treino = None
        self.__y_teste = None
        self.__classificador = self.classeClassificador()(random_state=42)
        pd.set_option('mode.chained_assignment',None)
        pass
    
    def __filtrarCampos(self):        
        self.__campos = self.__df[self.__nomeCampos]
        self.__alvo = self.__df[[self.nomeAlvo]]
    
    def __converterEmNumericas(self):
        le = LabelEncoder()
        for nome in self.__nomeCampos:
            self.__campos[nome] = le.fit_transform(self.__campos[nome])
        self.__alvo[self.nomeAlvo] = le.fit_transform(self.__alvo[self.nomeAlvo])
    
    def __dimensionando(self):
        mi_ma = MinMaxScaler()
        for nome in self.__nomeCampos:
            self.__campos[[nome]] = mi_ma.fit_transform(self.__campos[[nome]])
    
    def __balancear(self):
        oversample = SMOTE(random_state=42)
        self.__campos, self.__alvo = oversample.fit_resample(self.campos, self.alvo)        
    
    def __avaliarHoldout(self):
        x,y = (self.__campos, self.__alvo)        
        x_treino, x_teste, y_treino, y_teste = self.dadosSeparados
        self.__classificador.fit(x_treino, y_treino.values.ravel())
        self.__resultado = self.__classificador.predict(x_teste)
        holdout = {}
        for metrica in self.__metricas:
            algoritmo = self.__holdout[metrica]
            holdout[metrica] = np.mean(algoritmo(y_teste, self.__resultado))
        return holdout    
    
    def __avaliarCross(self):
        x,y = (self.__campos, self.__alvo)
        cross = {}
        for metrica in self.__metricas:
            cross[metrica] =  np.mean(cross_val_score(
                self.__classificador, x, y.values.ravel(), 
                cv=15, n_jobs=-1, scoring=metrica))
        return cross
    
    def __treinar(self):        
        holdout = self.__avaliarHoldout()
        cross = self.__avaliarCross()        
        return pd.DataFrame({
            'holdout': pd.Series(holdout.values(), index = holdout.keys()),
            'corss': pd.Series(cross.values(), index = cross.keys()),
        })
    
    def __separarDados(self):
        x,y = (self.__campos, self.__alvo)        
        self.__x_treino, self.__x_teste, self.__y_treino, self.__y_teste = train_test_split(x,y,
            test_size=0.20, random_state=42)        
    
    def classeClassificador(self): pass
    
    @property
    def df(self):
        return self.__df
    
    @df.setter
    def df(self, df):
        self.__df = df
        
    @property
    def classificador(self):
        return self.__classificador
    
    @property
    def nomeAlvo(self):
        return self.__nomeAlvo
    
    @property
    def balanceada(self)->bool:
        return self.__balanceada
    @balanceada.setter
    def balanceada(self, balanceada):
        self.__balanceada = balanceada
    
    @property
    def metricas(self):
        return self.__metricas
    @metricas.setter
    def metricas(self, metricas):
        self.__metricas = metricas
        
    @property
    def nomeCampos(self):
        return self.__nomeCampos
    @nomeCampos.setter
    def nomeCampos(self,nomeCampos):
        self.__nomeCampos = nomeCampos
        
    @property
    def campos(self):
        return self.__campos
    
    @property
    def alvo(self):
        return self.__alvo
    
    @property
    def resultado(self):
        return self.__resultado
    
    @property
    def dadosSeparados(self):
        return (
            self.__x_treino, 
            self.__x_teste, 
            self.__y_treino, 
            self.__y_teste            
        )
    
    def iniciar(self):        
        self.__alvo = self.__df[[self.__nomeAlvo]]
        self.__filtrarCampos()
        self.__converterEmNumericas()
        self.__dimensionando()
        if self.balanceada:
            self.__balancear()
        self.__separarDados()
        return self.__treinar()
        
        
        