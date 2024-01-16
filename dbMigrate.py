from pymongo import MongoClient
from tinydb import TinyDB, Query
import os

DB_FILE = "shopify_apps.json"
db = TinyDB(DB_FILE)

def getDatabase():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/shopifyAppMarketplace"
 
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)
 
    # Create the database for our example (we will use the same database throughout the tutorial
    return client['shopifyAppMarketplace']

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
    # Get the database
    dbname = getDatabase()
    collectionName = dbname["apps"]

    apps = db.all()
    
    for app in apps:
        collectionName.insert_many([app])