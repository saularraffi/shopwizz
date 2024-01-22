"""
- RFI score variables
    - Rating of the app (lower the better)
	- Number of reviews (higher the better) (normalize data)
	- Summed scores of 3 top problems???
	- Frequency of top problem
	- Date of poor reviews vs good reviews (once review dates are added)
    - Launch date of app (older the better) (normalize data)
	- Rating skew (more skewed to the bottom better than skewed to the middle??)

RFI = (b(Review Count) / a(Rating)) + c(Frequency)  + d(Launch Days)
Frequency = a(Frequency1) + b(Frequency2) + c(Frequency2)

RFI = (aR * bC) + cF + dD
F = aF1 + bF2 + cF3
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from math import floor

launchDateOffsetMinMax = ()
reviewCountsMinMax = ()
rfiScoresMinMax = ()

def getDatabase():
    CONNECTION_STRING = "mongodb://localhost:27017/shopifyAppMarketplace"
    client = MongoClient(CONNECTION_STRING)
    return client['shopifyAppMarketplace']

def normalize(x, xMin, xMax, multiplier):
    return round(((x - xMin) / (xMax - xMin)) * multiplier, 1)

def getLaunchDateOffsetList(apps):
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

def setMinsAndMaxes(apps):
    global launchDateOffsetMinMax
    global reviewCountsMinMax

    launchDateOffsetList = getLaunchDateOffsetList(apps)
    reviewsCountList = getReviewsCountList(apps)

    launchDateOffsetMinMax = (min(launchDateOffsetList), max(launchDateOffsetList))
    reviewCountsMinMax = (min(reviewsCountList), max(reviewsCountList))

def getDaysOffset(dateString):
    try:
        date = datetime.strptime(dateString, '%m-%d-%Y').date()
        today = datetime.today().date()
        offset = today - date
        return offset.days
    except Exception as e:
        return -1

def getAppVariableData(app, reviews):
    rating = app['rating']
    frequencies = [0, 0, 0]
    
    offset = getDaysOffset(app['dateLaunched'])
    launchDayOffset = offset if offset != -1 else 0
    normalizedLaunchDaysOffset = normalize(launchDayOffset, launchDateOffsetMinMax[0], launchDateOffsetMinMax[1], 100)
    
    reviewCount = app['reviewCount'] if app['reviewCount'] is not None else 0
    reviewCountNormalized = normalize(reviewCount, reviewCountsMinMax[0], reviewCountsMinMax[1], 1000)
    
    return (rating, normalizedLaunchDaysOffset, reviewCountNormalized, frequencies)

def getRfiScore(rating, launchDayOffset, reviewCount, frequencies):
    a = 5
    b = 8
    c = 7
    d = 2
    c1 = 5
    c2 = 3
    c3 = 1

    frequencyScore = c1*frequencies[0] + c2*frequencies[1] + c3*frequencies[2]
    rfiScore = floor((a*reviewCount / b*rating) + c*frequencyScore + d*launchDayOffset)

    # print("review count:", reviewCount, a*reviewCount)
    # print("rating:", rating, b*rating)
    # print("frequency:", frequencyScore, c*frequencyScore)
    # print("launch day offset:", launchDayOffset, d*launchDayOffset)
    # print("RFI Score:", rfiScore, "\n")

    return rfiScore

def test():
    id = '65aea2afc4b6ba8b7ad8f051'
    app = appsCollection.find_one({'_id': ObjectId(id)})
    reviews = reviewsCollection.find_one({'appId': ObjectId(id)})
    (rating, launchDayOffset, reviewCount, frequencies) = getAppVariableData(app, reviews)

if __name__ == "__main__":
    dbname = getDatabase()
    appsCollection = dbname["apps"]
    reviewsCollection = dbname["reviews"]
    apps = list(appsCollection.find({}))
    setMinsAndMaxes(apps)

    rfiScores = []

    for app in apps:
        reviews = reviewsCollection.find_one({'appId': ObjectId(app['_id'])})
        (rating, launchDayOffset, reviewCount, frequencies) = getAppVariableData(app, reviews)
        
        if reviewCount > 0:
            rfiScore = getRfiScore(rating, launchDayOffset, reviewCount, frequencies)
            rfiScores.append(rfiScore)
    
    rfiScoresMinMax = (min(rfiScores), max(rfiScores))
    normalizedRfiScores = []
    for score in rfiScores:
        normalizedScore = normalize(score, rfiScoresMinMax[0], rfiScoresMinMax[1], 1000)
        normalizedRfiScores.append(int(normalizedScore))
    
    normalizedRfiScores.sort()
    print(normalizedRfiScores)