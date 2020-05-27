# Essa biblioteca serve para tranformar os dados de aquisição a partir de funções estatísticas
import numpy as np
from scipy.signal import hilbert

class Functions():

    def __init__(self):
        self.functions = {

            'IEMG': self.IEMG,
            'MAV': self.MAV,
            'SSI': self.SSI,
            'RMS': self.RMS,
            'LOG': self.LOG,
            'WL': self.WL,
            'AAC': self.AAC,
            'DASDV': self.DASDV

        }

    @staticmethod
    def removeOffset(data):
        data -= np.mean(data)
        return data

    @staticmethod
    def rectifier(data):
        return np.absolute(data)

    @staticmethod
    def envelop(data):
        analytic_signal = hilbert(data)
        return np.abs(analytic_signal)

    @staticmethod
    def IEMG(x):
        return np.sum(np.abs(x))
    
    @staticmethod
    def MAV(x):
        return np.sum(np.abs(x))/np.shape(x)[0]
    
    @staticmethod
    def SSI(x):
        return np.sum(np.power(x, 2))/(np.shape(x)[0]-1)

    @staticmethod
    def RMS(x):
        return np.sqrt(np.sum(np.power(x, 2))/np.shape(x)[0])

    @staticmethod
    def LOG(x):
        return np.exp(np.sum(np.log(np.abs(x)))/np.shape(x)[0])

    @staticmethod
    def WL(x):
        return np.sum(np.abs(x[1:]-x[:-1]))

    @staticmethod
    def AAC(x):
        return np.sum(np.abs(x[1:]-x[:-1]))/np.shape(x)[0]

    @staticmethod
    def DASDV(x):
        return np.sqrt(np.sum(np.power(x[1:]-x[:-1], 2))/(np.shape(x)[0]-1))
    
    def transform(self, data, functions):
        # O array dados irá ter em cada linha, um determinado janelamento
        d = {}
        
        for k, _ in functions.items():
            d[k] = []
            
            for i in range(np.shape(data)[0]):
                d[k].append(self.functions[k](data[i,:]))
            d[k] = np.asarray(d[k]).reshape(-1,1)
        
        return d


class Preprocessing:
    
    def __init__(self, aquisition):
        self.database = aquisition.database
        self.__nChannels = aquisition.nChannels
        self.__batchsize = aquisition.batchSize
        self.__preprocessingFunctions = {}
        self.fPreprocessing = Functions()
    
    def getDataFromDatabase(self):
        self.dataChannel = {}
        
        for i in self.database.push_data():
            for k, v in i['data'].items():
                try:
                    self.dataChannel[k].append(v)
                except:
                    self.dataChannel[k] = []
                    self.dataChannel[k].append(v)
        
        self.preprocessedData = {}
        for k, v in self.dataChannel.items():
            
            self.dataChannel[k] = np.asarray(v).reshape(-1, self.__batchsize)
            self.preprocessedData[k] = self.fPreprocessing.transform(self.dataChannel[k], self.__preprocessingFunctions)