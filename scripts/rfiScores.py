from util import normalize, getDaysOffset
from rfiCalculator import RfiCalculator
from bson.objectid import ObjectId
from pymongo import MongoClient
import os

DB_CONNECTION_STRING = "mongodb://localhost:27017/shopifyAppMarketplace"
DB_NAME = 'shopifyAppMarketplace'
APP_COLLECTION_NAME = "apps"
REVIEWS_COLLECTION_NAME = "reviews"
LOG_FILE = os.path.join("logs", "rfiScores.log")

rfiScoresMinMax = ()

def getDatabase():
    client = MongoClient(DB_CONNECTION_STRING)
    return client[DB_NAME]
    
def getDaysActiveList(apps):
    offsets = []
    for app in apps:
        launchDate = app['dateLaunched']
        offset = getDaysOffset(launchDate)
        if offset != -1:
            offsets.append(offset)
    return offsets

def getReviewsCountList(apps):
    reviewCounts = []
    for app in apps:
        count = app['reviewCount']
        if count is not None:
            reviewCounts.append(count)
    return reviewCounts

def getMinsAndMaxes(apps):
    daysActiveList = getDaysActiveList(apps)
    reviewsCountList = getReviewsCountList(apps)

    daysActiveMinMax = (min(daysActiveList), max(daysActiveList))
    reviewCountsMinMax = (min(reviewsCountList), max(reviewsCountList))

    return (daysActiveMinMax, reviewCountsMinMax)

def logDbInsertError(appId, error):
    with open(LOG_FILE, 'a') as logFile:
        logFile.write("Failed to insert analysis for app " + str(appId) + ": " + str(error) + "\n")

def insertAnalysisInDb(appId, appsCollection, rfiScore):
    try:
        appsCollection.update_one({
            "_id": ObjectId(appId) 
        },
        { 
            "$set": { "rfiScore": rfiScore } 
        })
    except Exception as e:
        logDbInsertError(appId, e)

if __name__ == "__main__":
    dbname = getDatabase()
    appsCollection = dbname[APP_COLLECTION_NAME]
    reviewsCollection = dbname[REVIEWS_COLLECTION_NAME]
    apps = list(appsCollection.find({}))
    (daysActiveMinMax, reviewCountsMinMax) = getMinsAndMaxes(apps)

    RfiCalculator.daysActiveMinMax = daysActiveMinMax
    RfiCalculator.reviewCountsMinMax = reviewCountsMinMax

    rfiScores = []
    appIds = []

    for app in apps:
        rfiCalculator = RfiCalculator(app)
        rfiScore = rfiCalculator.getScore()
        rfiScores.append(rfiScore)
        appIds.append(app["_id"])

    rfiScoresMinMax = (min(rfiScores), max(rfiScores))
    normalizedRfiScores = []
    for score in rfiScores:
        normalizedScore = normalize(score, rfiScoresMinMax[0], rfiScoresMinMax[1], 1000)
        normalizedRfiScores.append(int(normalizedScore))
    
    for index, score in enumerate(normalizedRfiScores):
        print("Adding RFI score of " + str(score) + " to app with id " + str(appIds[index]))
        insertAnalysisInDb(appIds[index], appsCollection, score)