import numpy as np
from preprocessing import Functions
from sklearn.preprocessing import MinMaxScaler

# Essa classe irá tratar os dados de pré-processamento
class PreprocessingData:

    def __init__(self, data):
        self.data = data
        self.f = Functions()
    
    def updateData(self, data):
        self.data = data
    
    def preprocessData(self):
        channel = {}
        batshsize = 100
        contador = 0
        for d in self.data:
            contador +=1
            batshsize = d['data']['batsh_size']
            for k, v in d['data']['data'].items():
                try:
                    channel[k].append(v)
                except:
                    channel[k] = []
                    channel[k].append(v)
        
        
        self.preprocessedData = {}
        for k, v in channel.items():
            channel[k] = np.asarray(v).reshape(-1, batshsize)
            
            self.preprocessedData[k] = self.f.transform(channel[k], self.f.functions)
    
    def getRangeXAxis(self, channel, function):
        data = self.preprocessedData[channel][function]
        max_ = np.max(data)
        min_ = np.min(data)
        return (np.asscalar(min_), np.asscalar(max_))
    
    def getData(self, channel, function):
        return self.preprocessedData[channel][function]
         
