from functools import reduce
import pandas as pd

class Tratamento:
    def __init__(self, org: str, dst: str, tCursos, campos):
        self.__nomeArqOrig: str = org
        self.__nomeArqDest:str = dst
        self.__tipoCursos = tCursos
        self.__campos = campos
        self.__qtdCampos = 0
        self.__qtdRegistros = 0
        self.__instituicao = []
        pass
    
    def __abrirOrig(self):        
        return pd.read_csv(self.__nomeArqOrig)
    
    def __removerNulos(self, df):
        for coluna in list(df):
            df = df.loc[df[coluna].notnull()]
        return df
    
    def __filtrarCursos(self, df):
        return df.loc[
            reduce(lambda a, b: a | (df['tipo_curso'] == b), self.__tipoCursos, False)
        ]
    
    def __filtrarIdade(self, df):
        return df.loc[ (df['idade'] >= 10) & (df['idade'] <= 90) ]
    
    def __filtrarCampos(self, df):
        return df[self.__campos]
    
    def __filtrarInstituicao(self, df):
        print(self.__instituicao)
        if len(self.__instituicao) == 0:
            return df
        df = df[df['instituicao'].isin(self.__instituicao)]
        print(df['instituicao'])
        return df
    
    
    @property
    def nomeArqOrig(self)->str:
        return self.__nomeArqOrig
    @nomeArqOrig.setter
    def nomeArqOrig(self, nomeArqOrig: str):
        self.__nomeArqOrig = nomeArqOrig
        
    @property
    def nomeArqDest(self)->str:
        return self.__nomeArqDest
    @nomeArqDest.setter
    def nomeArqDest(self, nomeArqDest: str):
        self.__nomeArqDest = nomeArqDest
    
    @property
    def tipoCursos(self):
        return self.__tipoCursos
    @tipoCursos.setter
    def tipoCursos(self, tipoCursos):
        self.__tipoCursos = tipoCursos
    
    @property
    def campos(self):
        return self.__campos
    @campos.setter
    def campos(self, campos):
        self.__campos = campos
    
    @property
    def instituicao(self):
        return self.__instituicao
    @instituicao.setter
    def instituicao(self, instituicao):
        self.__instituicao = instituicao
    
    @property
    def qtdCampos(self)->int:
        return self.__qtdCampos
    
    @property
    def qtdRegistros(self)->int:
        return self.__qtdRegistros
    
    def processar(self):
        df = self.__abrirOrig()
        df = self.__removerNulos(df)
        df = self.__filtrarCursos(df)
        df  = self.__filtrarIdade(df)
        df = self.__filtrarInstituicao(df)
        df = self.__filtrarCampos(df)
        self.__qtdRegistros, self.__qtdCampos = df.shape
        df.to_csv(self.__nomeArqDest, index = False)
    pass