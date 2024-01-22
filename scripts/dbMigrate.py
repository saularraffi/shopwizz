from pymongo import MongoClient
from tinydb import TinyDB, Query
import dateutil.parser as dparser
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(SCRIPT_PATH, "..", "shopify_apps.json")
db = TinyDB(DB_FILE)

def getDatabase():
    CONNECTION_STRING = "mongodb://localhost:27017/shopifyAppMarketplace"
    client = MongoClient(CONNECTION_STRING)
    return client['shopifyAppMarketplace']

def insertAppData(collection, app):
    del app['reviews']
    dateString = app['dateLaunched']
    date = ""
    try:
        date = dparser.parse(dateString,fuzzy=True).date().strftime("%m-%d-%Y")
    except:
        pass
    finally:
        app['dateLaunched'] = date
        mongoApp = collection.insert_one(app)
        return mongoApp.inserted_id

def insertReviews(collection, reviews, appId):
    collection.insert_one({
        'appId': appId,
        'reviews': reviews
    })

def insertMarketplaceData(collection):
    categoriesTable = set()
    for app in apps:
        for category in app['categories']:
            if category not in categoriesTable:
                categoriesTable.add(category)
    
    numberOfApps = len(apps)
    categories = list(categoriesTable)
    categories.sort()

    collection.insert_one({
        'numberOfApps': numberOfApps,
        'categories': categories
    })

if __name__ == "__main__":   
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
        appId = insertAppData(appsCollection, app)
        insertReviews(reviewsCollection, reviews, appId)

    insertMarketplaceData(marketplaceCollection)