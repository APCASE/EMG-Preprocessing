import pymongo
import time
class Database_emg:
    
    def __init__(self, database_name, col_name, url=None):
        self.__database_name = database_name
        self.__col_name = col_name

        self.__client = pymongo.MongoClient(url)
        self.__db = self.__client[self.__database_name]
        self.__col = self.__db[self.__col_name]
        
        self.__id = 1

        #self.clean_database()

    def save(self, data):
        datal = {}
        for k, v in data.items():
            datal[k] = list(v)
        dataDict = {"_id":self.__id, "data":datal}
        result = self.__col.insert_one(dataDict)
        if result.acknowledged:
            self.__id+=1
        else:
            print("Problema ao salvar os dados, verifique a classe database")
    
    def push_data(self):
        return self.__col.find()
    
    def clean_database(self):
        self.__db[self.__col_name].drop()

