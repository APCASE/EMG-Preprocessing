import numpy as np
from preprocessing import Functions
from sklearn.preprocessing import MinMaxScaler

# Essa classe irá tratar os dados de pré-processamento
class PreprocessingData:

    def __init__(self, aquisition):
        # Pegando os dados da classe database
        self.database = aquisition.database
        # Pegando o numero de canais utilizados na aquisição
        self.__nChannels = aquisition.nChannels
        
        self.__batchsize = aquisition.batchSize
        # Dicionário para selecionar as funções de pré-processmento que serão utilizadas
        self.__preprocessingFunctions = {}
        self.fPreprocessing = Functions()

    def getDataFromDatabase(self):
        '''
        Método para pegar os dados do database e aplicar as funções de pré-processamento
        '''
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
    
    def getMinMaxRange(self, channel, function):
        '''
        Método para retornar os pontos máximos e mínimos de um conjunto de dados
        Args:
            channel: A chave do canal utilizado
            function: Chave da função que será utilizada  
        '''
        self.scaler = MinMaxScaler((0, 100))
        self.scaler.fit(self.preprocessedData[str(channel)][function].reshape(-1,1))
        min_ = np.min(self.scaler.transform(self.preprocessedData[str(channel)][function]))
        max_ = np.max(self.scaler.transform(self.preprocessedData[str(channel)][function]))

        return (np.asscalar(min_),np.asscalar(max_))
    
    def setBias(self, value):
        '''
        Esse método será utilizado para configurar o bias para se fazer os rótulos do dataset de treinamento
        Args:
            value: valor inteiro de 0 a 100
        '''

        self.__bias = self.scaler.inverse_transform(np.array(value).reshape(-1, 1))
    
    def setPreprocessingFunction(self, functions):
        '''
        Esse método irá configurar as funções de pré-processamento que serão utilizadas para construção do dataset
        '''
        self.__preprocessingFunctions = []
        for f in functions:
            self.__preprocessingFunctions.append(f)
    
    @staticmethod
    def generateBinaryClassifier(data, bias, nMovimento):
        '''
        Método para detectar um movimento e atribuir um valor ao mesmo

        Args:
            data: Um array numpy
            bias: um valor float para determinar o movimento
            nMovimento: inteiro para ser atribuido ao movimento
        '''
        binary = []

        for i in range(np.shape(data)[0]):
            if data[i]>bias:
                binary.append(nMovimento)
            else:
                binary.append(0)
        
        return np.asarray(binary)