from pymongo import MongoClient
from tinydb import TinyDB, Query
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(SCRIPT_PATH, "..", "shopify_apps.json")
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
    appsCollection = dbname["apps"]
    reviewsCollection = dbname["reviews"]
    marketplaceCollection = dbname["marketplacestats"]

    appsCollection.drop()
    reviewsCollection.drop()
    marketplaceCollection.drop()

    apps = db.all()

    for app in apps:
        reviews = app['reviews']
        del app['reviews']
        mongoApp = appsCollection.insert_one(app)
        reviewsCollection.insert_one({
            'appId': mongoApp.inserted_id,
            'reviews': reviews
        })

    categoriesTable = set()
    for app in apps:
        for category in app['categories']:
            if category not in categoriesTable:
                categoriesTable.add(category)
    
    numberOfApps = len(apps)
    categories = list(categoriesTable)
    categories.sort()

    marketplaceCollection.insert_one({
        'numberOfApps': numberOfApps,
        'categories': categories
    })