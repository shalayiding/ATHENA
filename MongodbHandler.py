# handle different mongodb event  

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import json
import apikeys as key




class MongodbHandler:
    def __init__(self,db_url,db_name,collection_name) -> None:
        self.clint = MongoClient(db_url,server_api = ServerApi('1'))
        self.db = self.clint[db_name]
        self.collection = self.db[collection_name]

    
    #change the existing db and collection 
    def Switch_db_collection(self,db_name,collection_name):
        self.db = self.clint[db_name]
        self.collection = self.db[collection_name]
        
    
    # insert new user to the mongo db         
    def Insert_one_User(self,post):
        try :
            status = self.collection.insert_one(post)
            return status.inserted_id
        except Exception as e :
            print(e)
            return None
         
    # check if user exist in the mongodb    
    def check_user(self,discord_id):
        try :
            query = {'discord_id' : discord_id}
            status = self.collection.find_one(query)
            return status is not None
        except Exception as e:
            print(e)
            return False

    






client = MongoClient(key.MongoDB_uri,Server_api = ServerApi('1'))







try:
    with open('Questions.json', 'r') as file:
        questions = json.load(file)
        print(questions)
    for db_name in client.list_database_names():
        print(f"Database: {db_name}")
        db = client[db_name]
        if db_name == "Interview_Questions":
            questions_collection = db['technical_interview_questions']
            questions_collection.delete_many({})
            questions_collection.insert_many(questions)
        
        for collection_name in db.list_collection_names():
            print(f"  Collection: {collection_name}")

except Exception as e:
    print(e)

