import numpy as np
from preprocessing import Functions
import pandas as pd

# Essa classe irá tratar os dados de pré-processamento
class PreprocessingData:

    def __init__(self, data):
        self.data = data
        self.f = Functions()
    
    def updateData(self, data):
        self.data = data
    
    def preprocessData(self):
        self.channel_rawData = {}
        batshsize = 100
        
        for d in self.data:
            
            self.batshsize = d['data']['batsh_size']
            self.nChannels = d['data']['n_channels']
            for k, v in d['data']['data'].items():
                try:
                    self.channel_rawData[k].append(v)
                except:
                    self.channel_rawData[k] = []
                    self.channel_rawData[k].append(v)
        
        
        self.preprocessedData = {}
        for k, v in self.channel_rawData.items():
            self.channel_rawData[k] = np.reshape(np.asarray(v), (-1, self.batshsize))       
            self.preprocessedData[k] = self.f.transform(self.channel_rawData[k], self.f.functions)
    
    def getRangeXAxis(self, channel, function):
        data = np.reshape(self.preprocessedData[channel][function], (-1,1))
        max_ = np.shape(data)[0]
        min_ = 0
        return (min_, max_)
    
    def getData(self, channel, function):
        return self.preprocessedData[channel][function]
    
    def getRangeYAxis(self, channel, function):
        data = np.reshape(self.preprocessedData[channel][function], (-1,1))
        max_ = np.max(data)
        min_ = np.min(data)
        return (np.asscalar(min_), np.asscalar(max_))
    
    def exportToCSV(self, functions, label):
        data = {}
        for k, v in self.preprocessedData.items():
            data[k] = {}
            for f in functions:
                data[k][f] = v[f]

        df = pd.DataFrame(data)
        df.columns = ["Channel {}".format(c) for c in range(self.nChannels)]
        df.to_csv('signalPreprocessed.csv')

        df = pd.Series(self.channel_rawData)
        df.columns = ["Channel {}".format(c) for c in range(self.nChannels)]
        df.to_csv('signalRaw.csv')
        
        labels = {'label':label}
        df = pd.Series(labels)
        df.to_csv('label.csv')

        
         
