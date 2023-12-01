# handle different mongodb event  
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import apikeys as key
from datetime import datetime

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

    def find_section(self,discord_id):
        """ find section using discord_id

        Args:
            discord_id (_type_): discord id

        Returns:
            list : return the section in list
        """
        try :
            query = {'discord_id' : discord_id}
            result = self.collection.find_one(query)
            return result['section'] if result else None
        except Exception as e:
            print(e)
    
    def create_one_User(self,discord_name,discord_id):
        """create one user to database
        Args:
            discord_name (_type_): discord name
            discord_id (_type_): discrod id large int  
            sections (_type_): AI chat sections
        """
        try :
            query = {'discord_name':discord_name,'discord_id':discord_id,'sections':[]}
            self.collection.insert_one(query)
        except Exception as e :
            print(e)
    

    def create_one_section(self,discord_id,discord_name,bot_name):
        timestamp = datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
        self.section = {
            "discord_name":discord_name,
            "discord_id":discord_id,
            "bot_name":bot_name,
            "section_id": f"{discord_id}-{timestamp}",
            "messages":[]
        }
        

    def insert_user_message(self,user_message):
        timestamp = datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
        self.message = {
            'discord_input':user_message,
            'message_received':timestamp
        }
    
    def insert_bot_message(self,bot_message):
        timestamp = datetime.now().strftime("%Y/%m/%d/%H:%M:%S")
        self.message.update({'bot_message':bot_message,'message_sent':timestamp})
    
    def insert_message(self,discord_id):
        try :
            user_doc = self.collection.find_one({'discord_id': discord_id})
            if user_doc and 'sections' in user_doc:
                if not user_doc['sections'] :
                    user_doc['sections'].append(self.section)            
                    
                user_doc['sections'][-1]['messages'].append(self.message)
                query = {'discord_id':discord_id}
                update = {'$set':{'sections':user_doc['sections']}}
                self.collection.update_one(query,update)
        except Exception as e:
            print(e)
                                                                         
                                        
    def update_user_section(self,discord_id):
        """update user section using discord_id and section

        Args:
            discord_id (_type_): discord id 
            section (_type_): list of chat section with bot
        """
        try :
            query = {'discord_id':discord_id}
            update = {'$set':{'sections':self.section}}
            self.collection.update_one(query,update)
        except Exception as e:
            print(e)
    
    
# db = MongodbHandler(key.MongoDB_uri,'Users','discord_users')

# db.create_one_User('aken',discord_id='123')
# section = db.create_one_section('123','aken','vertexai')
# db.insert_message('123','who are you ?','I am good',section)
# db.insert_message('123','this is next chat','reqwrI am good',section)
# db.insert_message('123','this is third chat','I am gorewrwerod',section)