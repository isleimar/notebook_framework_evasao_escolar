import pandas as pd
# import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt

from scripts.analise_np import AnaliseNP
class GraficoNP:
    def __init__(self, aNp: AnaliseNP):
        self.__aNp: AnaliseNP = aNp
        self.__tamFonte: int = 12
        self.__tamFigura = (10,4)
        self.__largura = 0.9
    
    def __plotarGrafico(self, ax, graficos):
        for i, graf in graficos.items():                        
            field_label = self.__aNp.rotuloCampo
            chart = graf['df'].plot(
                ax = ax[i],
                kind ='bar', 
                figsize = self.tamFigura, 
                width = self.largura, 
                grid = True,
                stacked = graf['stacked'], 
                legend = graf['legend'], 
                fontsize=self.tamFonte)
            chart.grid(axis='x')
            chart.set_xlabel(
                field_label,
                fontdict={'fontsize':self.tamFonte})
            chart.set_title(
                graf['title'],
                fontdict={'fontsize':self.tamFonte})
            if graf['legend']:
                chart.get_legend().set_title('Categoria/Situação')
                chart.legend(fontsize=self.tamFonte, loc='lower center')
        
        
        
    @property
    def aNp(self)->AnaliseNP:
        return self.__aNp
    
    @property
    def tamFonte(self)->int:
        return self.__tamFonte
    @tamFonte.setter
    def tamFonte(self, tamFonte):
        self.__tamFonte = tamFonte
    
    @property
    def tamFigura(self):
        return self.__tamFigura
    @tamFigura.setter
    def tamFigura(self, tamFigura):
        self.__tamFigura = tamFigura
    
    @property
    def largura(self):
        return self.__largura
    @largura.setter
    def largura(self, largura):
        self.__largura = largura
     
    def mostrarGraficos(self):        
        grafics = {
            0: { 
                'df': self.__aNp.dadosQuant,
                'title': "QUANTIDADE POR CATEGORIA",
                'legend': False,
                'stacked': False,
            },
            1: { 
                'df': self.__aNp.dadosGrupo,
                'title': "QUANTIDADE POR {}".format(self.__aNp.rotuloCampo.upper()),
                'legend': False,
                'stacked': False,
            },
            2: { 
                'df': self.__aNp.dadosCategoria,
                'title': "QUANTIDADE POR CATEGORIA E {}".format(self.__aNp.rotuloCampo.upper()),
                'legend': True,
                'stacked': False,
            },         
            3: { 
                'df': self.__aNp.dadosCategoria,
                'title': "QUANTIDADE POR CATEGORIA E {}".format(self.__aNp.rotuloCampo.upper()),
                'legend': True,
                'stacked': True,
            },         
        }
        categories = self.aNp.categorias
        i = len(grafics)
        for category in categories:            
            df = self.__aNp.dadosSumario.copy()
            if set([category]).issubset(df.columns):
                df = df[category + '_%'].drop('TOTAL')                
                title = "PORCENTAGEM DE {}".format(category.upper())
                grafics[i] = {
                    'df':df,
                    'title':title,
                    'legend': False,
                    'stacked': False,
                }
                i += 1
        fig, ax = plt.subplots(len(grafics),1)
        self.__plotarGrafico(ax, grafics)
        plt.subplots_adjust(bottom=0.1, top=0.6,hspace=0.4)
        
    
    def graficoPorcentagem(self, categoria: str):        
        df = self.__aNp.dadosSumario.copy()
        df = df[categoria + '_%'] * 100     
        title = "PORCENTAGEM DE {}".format(categoria.upper())
        return self.__criarGrafico(df,title,False)