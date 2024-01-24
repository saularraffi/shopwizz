from util import normalize, getDaysOffset
from rfiCalculator import RfiCalculator
from pymongo import MongoClient

DB_CONNECTION_STRING = "mongodb://localhost:27017/shopifyAppMarketplace"
DB_NAME = 'shopifyAppMarketplace'
APP_COLLECTION_NAME = "apps"
REVIEWS_COLLECTION_NAME = "reviews"

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

if __name__ == "__main__":
    dbname = getDatabase()
    appsCollection = dbname[APP_COLLECTION_NAME]
    reviewsCollection = dbname[REVIEWS_COLLECTION_NAME]
    apps = list(appsCollection.find({}))
    (daysActiveMinMax, reviewCountsMinMax) = getMinsAndMaxes(apps)

    RfiCalculator.daysActiveMinMax = daysActiveMinMax
    RfiCalculator.reviewCountsMinMax = reviewCountsMinMax

    rfiScores = []

    for app in apps:
        rfiCalculator = RfiCalculator(app)
        rfiScore = rfiCalculator.getScore()
        rfiScores.append(rfiScore)
   
    rfiScoresMinMax = (min(rfiScores), max(rfiScores))
    normalizedRfiScores = []
    for score in rfiScores:
        normalizedScore = normalize(score, rfiScoresMinMax[0], rfiScoresMinMax[1], 1000)
        normalizedRfiScores.append(int(normalizedScore))
    
    normalizedRfiScores.sort()
    print(normalizedRfiScores)