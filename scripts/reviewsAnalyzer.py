from gptApi import GptReviewAnalyzer
from bson.objectid import ObjectId
from pymongo import MongoClient
from time import sleep
import os
    
DB_CONNECTION_STRING = "mongodb://localhost:27017/shopifyAppMarketplace"
DB_NAME = 'shopifyAppMarketplace'
APP_COLLECTION_NAME = "apps"
REVIEWS_COLLECTION_NAME = "reviews"
LOG_FILE = os.path.join("logs", "reviewsAnalyzer.log")

def getDatabase():
    client = MongoClient(DB_CONNECTION_STRING)
    return client[DB_NAME]

def getTokenCount(reviews):
    totalChars = 0
    for review in reviews:
        totalChars += len(review)
    return totalChars/4

def getReviewsFromObj(reviewObj):
    allReviews = reviewObj['reviews']
    reviews = []
    for star, _ in allReviews.items():
        if star == "1-star" or star == "2-star" or star == "3-star":
            for review in allReviews[star]['content']:
                reviews.append(review)
    return reviews

def isValidAppToAnalyzeReviews(app):
    rating = app["rating"]
    reviewCount = app["reviewCount"]

    if rating is None or reviewCount is None:
        return False
    
    if rating > 4.5 or reviewCount == 0:
        return False

    return True

def logAnalysisError(reviewId, error):
	with open(LOG_FILE, 'a') as logFile:
		logFile.write("Failed to analyze reviews for entry " + str(reviewId) + ": " + str(error) + "\n")

def logDbInsertError(appId, error):
    with open(LOG_FILE, 'a') as logFile:
        logFile.write("Failed to insert analysis for app " + str(appId) + ": " + str(error) + "\n")

def getGptResponse(reviews, reviewId):
    response = {}
    try:
        reviewAnalyzer = GptReviewAnalyzer(reviews)
        response = reviewAnalyzer.run()            
    except Exception as e:
        logAnalysisError(reviewId, e)
    return response

def insertAnalysisInDb(appId, appsCollection, analysisObj):
    try:
        appsCollection.update_one({
            "_id": ObjectId(appId) 
        },
        { 
            "$set": analysisObj 
        })
    except Exception as e:
        logDbInsertError(appId, e)

if __name__ == "__main__":
    dbname = getDatabase()
    appsCollection = dbname[APP_COLLECTION_NAME]
    reviewsCollection = dbname[REVIEWS_COLLECTION_NAME]
    reviewObjs = list(reviewsCollection.find({}))

    count = 1
    for reviewObj in reviewObjs:
        reviewId = ObjectId(reviewObj["_id"])
        appId = reviewObj["appId"]

        associatedApp = appsCollection.find_one({"_id": appId})
        reviews = getReviewsFromObj(reviewObj)

        if not isValidAppToAnalyzeReviews(associatedApp) or len(reviews) == 0:
            continue

        response = getGptResponse(reviews, reviewId)

        if response == {}:
            continue

        insertAnalysisInDb(associatedApp["_id"], appsCollection, response)

        print("[+] {}/1635: Finished analyzing {}".format(count, reviewId))
        
        count += 1
        sleep(60)