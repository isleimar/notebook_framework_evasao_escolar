from scripts.data_base import DataBase
import pandas as pd

class AnaliseNP:
    def __init__(self, db: DataBase, tabela: str, campo: str, 
                 tiposCurso = [], 
                 categorias = ['Evadidos','Concluintes', 'Em curso'],
                 ordenar = []):
        self.__db = db
        self.__tabela:str = tabela
        self.__campo:str = campo        
        self.__rotuloCampo:str = ''
        self.__tiposCurso = tiposCurso
        self.__ordenar = ordenar
        self.__filtro = {
            'categoria_situacao': categorias,
            campo: True,
            'tipo_curso': (len(tiposCurso) > 0) or (campo == 'tipo_curso'),
            'instituicao': '',
            'unidade_ensino': '',
            'nome_curso': '',
        }
        self.__dados = None
        self.__dadosCategoria = None
        self.__dadosGrupo = None
        self.__dadosSumario = None
        self.__dadosQuant = None
        self.__total: int = 0
    
    def __createFields(self):
        s = []
        gf = []
        for k, v in self.filtro.items():
            if v :
                if type(v) is str:
                    s.append("({} = '{}')".format(k,v))            
                elif type(v) is list:
                    s.append("({} IN ({}))".format(
                        k,','.join(map(str,["'{}'".format(i) for i in v]))))
                if (type(v) is bool and v) or (not type(v) is bool):
                    gf.append(k)
        filter_sql = " AND ".join(map(str,s))
        fields = ", ".join(map(str,gf))
        return fields, filter_sql
        
    
    def __criarStringBusca(self):        
        fields, filter_sql = self.__createFields()
        sql = "SELECT {0}, sum(quant_grupo) AS quant_grupo" \
            " FROM {1} " \
            " WHERE {2} " \
            " GROUP BY {0}" \
            " ALLOW FILTERING;".format(
                fields,
                self.tabela,
                filter_sql)
        print(sql)
        return sql
    
    def __consultaTotal(self, df):
        self.__total = df['quant_grupo'].sum()
    
    def __consulta(self):        
        df = self.db.execute(self.__criarStringBusca())        
        # Filtrar Curso
        df = self.__filtrarProCurso(df)        
        self.__dados = df
        self.__consultaTotal(df)
        # Agrupar Valors
        self.__agruparValores(df)        
        self.__dadosCategoria, self.__dadosGrupo, self.__dadosQuant = self.__agruparValores(df)
        self.__calcularSumario()
    
    def __filtrarProCurso(self, df):
        if self.tiposCurso:
            return df[df['tipo_curso'].isin(self.tiposCurso)]        
        return df.copy()        
    
    def __agruparValores(self, df):
        field = self.campo
        #Agrupar
        df_cat_bas = df.groupby(['categoria_situacao']
            ).sum('quant_grupo').reset_index()
        df_cat = df.groupby(['categoria_situacao',field]
            ).sum('quant_grupo').reset_index()
        df_grp = df.groupby([field]
            ).sum('quant_grupo').reset_index() 
        #Criando Ordem
        if len(self.ordenar) == 0:
            order = list(df_grp.sort_values('quant_grupo', ascending=False)[field])
            self.__ordenar = order
        else:
            order = self.ordenar
        sort_keys = {v:k for k,v in enumerate(order)}
        func_sort = lambda e: sort_keys[e]        
        # Ordenar     
        df_cat = df_cat.pivot_table('quant_grupo',[field],'categoria_situacao'
            ).sort_values(by=field, key=lambda col: col.map(func_sort))
        df_grp = df_grp.pivot_table('quant_grupo',[field]
            ).sort_values(by=field, key=lambda col: col.map(func_sort))
        df_cat_bas = df_cat_bas.pivot_table('quant_grupo',['categoria_situacao']
            ).sort_values(by='quant_grupo', ascending = False)
        return df_cat, df_grp, df_cat_bas
    
    def __calcularSumario(self):
        field = self.campo
        df = self.dados
        df = df.groupby(['categoria_situacao',field]).sum('quant_grupo').reset_index()
        categories = list(df['categoria_situacao'].unique())
        total = df['quant_grupo'].sum()
        df_res = self.dadosCategoria.copy() 
        df_res['total'] = df_res[categories].sum(axis=1)
        dic_total = {}
        dic_total['total'] = total
        for category in categories:
            df_res[category + '_%'] = (df_res[category] / df_res['total']) * 100
            sum_cat = df_res[category].sum()
            dic_total[category] = sum_cat
            dic_total[category + '_%'] = (sum_cat / total) * 100
        dic_total['total_%'] = 100
        df_res['total_%'] = (df_res['total'] / total) * 100
        df_total = pd.DataFrame([list(dic_total.values())], columns = list(dic_total.keys()), index = ['TOTAL'])        
        self.__dadosSumario = pd.concat([df_res,df_total])
        
    @property
    def db(self)->DataBase:
        return self.__db;
    
    @db.setter
    def db(self, db):        
        self.__db = db
        
    @property
    def tabela(self)->str:
        return self.__tabela;
    
    @property
    def campo(self)->str:
        return self.__campo;
    
    @property
    def categorias(self):
        return self.__filtro['categoria_situacao']
    
    @property
    def tiposCurso(self)->str:
        return self.__tiposCurso;
    
    @property
    def ordenar(self):
        return self.__ordenar
    
    @property
    def rotuloCampo(self)->str:
        return self.__rotuloCampo;
    @rotuloCampo.setter
    def rotuloCampo(self, rotuloCampo):
        self.__rotuloCampo = rotuloCampo
    
    @property
    def filtro(self):
        return self.__filtro
    
    @property
    def dados(self):
        return self.__dados
    
    @property
    def dadosCategoria(self):
        return self.__dadosCategoria
    
    @property
    def dadosGrupo(self):
        return self.__dadosGrupo
    
    @property
    def dadosSumario(self):
        return self.__dadosSumario
    
    @property
    def dadosQuant(self):
        return self.__dadosQuant
    
    @property
    def instituicao(self):
        return self.filtro['instituicao']
    @instituicao.setter
    def instituicao(self, instituicao):
        self.filtro['instituicao'] = instituicao
    
    @property
    def unidadeEnsino(self):
        return self.filtro['unidade_ensino']
    @unidadeEnsino.setter
    def unidadeEnsino(self, unidadeEnsino):
        self.filtro['unidade_ensino'] = unidadeEnsino
    
    @property
    def nomeCurso(self):
        return self.filtro['nome_curso']
    @nomeCurso.setter
    def nomeCurso(self, nomeCurso):
        self.filtro['nome_curso'] = nomeCurso
        
    @property
    def total(self)->int:
        return self.__total
    
    def executarConsulta(self):
        self.__consulta()
    
    pass