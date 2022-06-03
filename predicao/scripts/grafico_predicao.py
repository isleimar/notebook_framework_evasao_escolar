from scripts.predicao import Predicao
from matplotlib import pyplot as plt
from sklearn.metrics import plot_confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve
from sklearn.metrics import RocCurveDisplay
import pandas as pd

class GraficoPredicao:
    def __init__(self, preditores):
        self.__preditores = preditores
        pd.set_option('mode.chained_assignment',None)
        
    def __plotMatizConfusao(self, preditor:Predicao, ax):        
        x_treino, x_teste, y_treino, y_teste = preditor.dadosSeparados
        plot_confusion_matrix(preditor.classificador,
                              x_teste,
                              y_teste,
                              ax =ax,
                              cmap='Blues',
                              display_labels=['Concluidos','Evadidos'])
        ax.title.set_text(type(preditor.classificador).__name__)
    
    def __plotCurvaROU(self, preditor:Predicao, ax):
        x_treino, x_teste, y_treino, y_teste = preditor.dadosSeparados
        resultado = preditor.resultado
        fpr, tpr, _ = roc_curve(y_teste, resultado)
        roc_display = RocCurveDisplay(fpr=fpr, tpr=tpr).plot(ax = ax)
        ax.title.set_text(type(preditor.classificador).__name__)
    
    def mostrarGraficos(self):
        qtd = len(self.__preditores)
        fig, axes = plt.subplots(nrows = len(self.__preditores), ncols = 2, figsize=(10,qtd * 5))
        i = 0
        for preditor in self.__preditores:
            self.__plotMatizConfusao(preditor, axes[i][0])
            self.__plotCurvaROU(preditor, axes[i][1])
            i += 1
        plt.tight_layout()
        plt.show()
        