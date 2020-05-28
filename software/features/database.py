import pymongo
from datetime import datetime
class Database_emg:
    
    def __init__(self, user_name, URI, port):
        
        self.user_name = user_name        
        self.URI = URI
        self.port = port
        self.is_connected = False

        self.col_name = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
        
        try:
            self.client = pymongo.MongoClient(URI, port)
            self.db = self.client[self.user_name]
            self.col = self.db[self.col_name]
            self.is_connected = True
            print('testes')
        except pymongo.errors.ServerSelectionTimeoutError as err:
            print('Erro ao se conectar com o dataset:\n\t{}'.format(err))

        self.id = 1

    def save(self, data, n_channels, frequency, batch_size):
        
        datal = {'user': self.user_name,'n_channels': n_channels, 
            'frequency': frequency, 'batsh_size': batch_size, 'data': {}}
        for k, v in data.items():
            datal['data'][k] = list(v)
        dataDict = {"_id":self.id, "data":datal}
        result = self.col.insert_one(dataDict)
        if result.acknowledged:
            self.id+=1
        else:
            print("Problema ao salvar os dados, verifique a classe database")
    
    def push_data(self, column):
        col = self.db[column]
        return col.find()
    
    def clean_database(self):
        self.db[self.col_name].drop()
    
    def update_time(self):
        self.current_date = datetime.utcnow()
    
    def getCollections(self):
        collections = self.db.list_collection_names()
        collections.sort(reverse=True)
        return collections
    
    
#d = Database_emg('Gleidson', None, None)
#collections = d.getCollections()
#print(d.push_data(collections[0])[0])
