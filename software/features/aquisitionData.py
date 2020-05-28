# Essa classe será utilizada para fazer aquisição dos dados do sinal emg.
# Assim como na digilent, os dados virão como um array com um batchsize pré-definido
# A classe será generalizada para n canais do circuito de aquisição

from collections import deque
import random
import numpy as np
import os
import json
import time
from plotlive import PlotLive
from database import Database_emg


class DataAquisition:

    def __init__(self, user_name, interval, frequency, batchSize, nChannels):
        self.user_name = user_name
        
        # TODO: Definir canais, tamanho do batchsize, intervalo de amostragem na plotagem
        self.interval = interval
        self.frequency = frequency
        self.batchSize = batchSize
        self.nChannels = nChannels

        # TODO: Implementar dados para o numero de canais especificado
        self.currentDataChannels = {}
        self.__x = {}
        for i in range(nChannels):
            self.currentDataChannels[str(i)] = deque(maxlen=(interval[1]-interval[0]))
            self.__x[str(i)] = []
        
        self._plot = None
        self.__c = 0
        # Banco de dados para armazenar dados dos canais
        self.database = Database_emg(user_name, None, None)
    
    def updateGraph(self, canvas):
        """
        Método para atualizar os dados aquisitados e o gráfico da janela de aquisição

        Args:
            Canvas: FigureCanvas da biblioteca PyQT5
        """
        # Inicializando plotagem caso o widget ainda não esteja definido
        if not(self._plot):
            self._plot = PlotLive(canvas, self.interval, self.nChannels)
        # Atualizando dados da aquisição
        self.updateData(self.generateDataTest(self.nChannels, self.batchSize))
        # Atualizando o widget
        self._plot.updateGraph(self.__x, self.currentDataChannels)

    def updateData(self, data):
        """
        Método para armazenar os dados da aquição em dataChannels e currentDataChannels.
        Args:
            data: Lista de nChannels X BatchSize
        """

        for i, d in enumerate(data):
            for j in d:
                # Atualizando dados da plotagem
                self.currentDataChannels[str(i)].append(j)

            # Essa seção evita de atualizar os eixos das abscissas quando esse já estiver preenchido
            if len(self.__x[str(i)]) != int(self.interval[1]-self.interval[0]):
                self.__x[str(i)] = [i for i in range(len(self.currentDataChannels[str(i)]))]
        
        self.__c+=self.batchSize
        # Salvando os dados da aquisição
        if not(self.__c%int(self.interval[1]-self.interval[0])):

            self.database.save(self.currentDataChannels, self.nChannels, self.frequency, self.batchSize)
            self.__c = 0

    @staticmethod
    def generateDataTest(nChannels, batchSize):
        """Método para gerar dados randomicamente.
        
        Args:
            nChannels: Numero de canais do circuito de aquisição
            batchSize: Tamanho do pacote à se receber dos canais de aquisição
        Returns:
            lista nChannels X batchSize em que cada linha corresponde a quantidade de canais
        """
        
        return [[random.random() for b in range(batchSize)] for c in range(nChannels)]
    
    @staticmethod
    def writeJson(file, data, directory="data"):
        """Método para salvar arquivo em JSON.
        
        Args:
            File: Arquivos onde os dados serão escritos
            data: Dados para salvar
            directory: Pasta onde os arquivos serão salvos
        """
        with open("./{}/{}.json".format(directory, file), "w") as writeFile:
            json.dump(data, writeFile, indent=4)
