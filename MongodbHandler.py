# handle different mongodb event  
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import apikeys as key


class MongodbHandler:
    def __init__(self,db_url,db_name,collection_name) -> None:
        """Init connect the mongodb to database and collecton

        Args:
            db_url (string): Mongodb url link 
            db_name (string): Database name in 
            collection_name (string): collection in database 
        """
        self.clint = MongoClient(db_url,server_api = ServerApi('1'))
        self.db = self.clint[db_name]
        self.collection = self.db[collection_name]

    
    #change the existing db and collection 
    def Switch_db_collection(self,db_name,collection_name):
        """switch to different database and collection

        Args:
            db_name (string):database name
            collection_name (sring): collection name
        """
        self.db = self.clint[db_name]
        self.collection = self.db[collection_name]
        
        
    def Insert_one_User(self,discord_name,discord_id,history):
        """insert one user to database

        Args:
            discord_name (_type_): discord name
            discord_id (_type_): discrod id large int  
            history (_type_): AI chat history
        """
        try :
            query = {'discord_name':discord_name,'discord_id':discord_id,'history':history}
            self.collection.insert_one(query)
        except Exception as e :
            print(e)
    
      
    def check_user(self,discord_id):
        """check if the user in current collection

        Args:
            discord_id (_type_): discrod id

        Returns:
            Bool : if exist in the collection
        """
        try :
            query = {'discord_id' : discord_id}
            status = self.collection.find_one(query)
            return status is not None
        except Exception as e:
            print(e)
            return False

    def find_history(self,discord_id):
        """ find history using discord_id

        Args:
            discord_id (_type_): discord id

        Returns:
            list : return the history in list
        """
        try :
            query = {'discord_id' : discord_id}
            result = self.collection.find_one(query)
            return result['history'] if result else None
        except Exception as e:
            print(e)


    def update_user_history(self,discord_id,history):
        """update user history using discord_id and history

        Args:
            discord_id (_type_): discord id 
            history (_type_): list of chat history with bot
        """
        try :
            query = {'discord_id':discord_id}
            update = {'$set':{'history':history}}
            self.collection.update_one(query,update)
        except Exception as e:
            print(e)
    
    

