"""
- RFI score variables
    - Rating of the app (lower the better)
	- Number of reviews (higher the better) (normalize data)
	- Summed scores of 3 top problems???
	- Frequency of top problem
	- Date of poor reviews vs good reviews (once review dates are added)
    - Launch date of app (older the better) (normalize data)
	- Rating skew (more skewed to the bottom better than skewed to the middle??)

RFI = a(Rating) * b(Review Count) + c(Frequency)  + d(Launch Days)
Frequency = a(Frequency1) + b(Frequency2) + c(Frequency2)

RFI = (aR * bC) + cF + dD
F = aF1 + bF2 + cF3
"""

from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

launchDateOffsetMinMax = ()
reviewCountsMinMax = ()

def getDatabase():
    CONNECTION_STRING = "mongodb://localhost:27017/shopifyAppMarketplace"
    client = MongoClient(CONNECTION_STRING)
    return client['shopifyAppMarketplace']

def normalize(x, xMin, xMax):
    return round(((x - xMin) / (xMax - xMin)) * 100, 1)

def getLaunchDateOffsetList(apps):
    offsets = []
    for app in apps:
        launchDate = app['dateLaunched']
        offset = getDaysOffset(launchDate)
        if offset != -1:
            offsets.append(offset)
    return offsets

def getReviewsCountList(allReviews):
    reviewCounts = []
    for reviews in allReviews:
        count = getReviewCount(reviews)
        reviewCounts.append(count)
    return reviewCounts

def setMinsAndMaxes(appsCollection, reviewsCollection):
    global launchDateOffsetMinMax
    global reviewCountsMinMax

    apps = appsCollection.find({})
    reviews = reviewsCollection.find({})

    launchDateOffsetList = getLaunchDateOffsetList(apps)
    reviewsCountList = getReviewsCountList(reviews)

    launchDateOffsetMinMax = (min(launchDateOffsetList), max(launchDateOffsetList))
    reviewCountsMinMax = (min(reviewsCountList), max(reviewsCountList))

def getRfiScore():
    x = [343,634,322,113,600,844]
    xMin = min(x)
    xMax = max(x)
    
    for num in x:
        print(normalize(num, xMin, xMax))

def getDaysOffset(dateString):
    try:
        date = datetime.strptime(dateString, '%m-%d-%Y').date()
        today = datetime.today().date()
        offset = today - date
        return offset.days
    except Exception as e:
        return -1

def getReviewCount(reviews):
    reviewCount = 0
    for star, _ in reviews['reviews'].items():
        count = reviews['reviews'][star]['count']
        reviewCount += count
    return reviewCount

def getAppVariableData(app, reviews):
    rating = app['rating']
    frequencies = [.53, .40, .21]
    launchDayOffset = getDaysOffset(app['dateLaunched'])
    normalizedLaunchDaysOffset = normalize(launchDayOffset, launchDateOffsetMinMax[0], launchDateOffsetMinMax[1])
    reviewCount = getReviewCount(reviews)
    reviewCountNormalized = normalize(reviewCount, reviewCountsMinMax[0], reviewCountsMinMax[1])
    
    return (rating, normalizedLaunchDaysOffset, reviewCountNormalized, frequencies)

def getRfiScore():
    pass

def test():
    id = '65aea2afc4b6ba8b7ad8f051'
    app = appsCollection.find_one({'_id': ObjectId(id)})
    reviews = reviewsCollection.find_one({'appId': ObjectId(id)})

    (rating, launchDayOffset, reviewCount, frequencies) = getAppVariableData(app, reviews)

    print("rating:", rating)
    print("days offset:", launchDayOffset)
    print("review count:", reviewCount)

if __name__ == "__main__":
    dbname = getDatabase()
    appsCollection = dbname["apps"]
    reviewsCollection = dbname["reviews"]
    setMinsAndMaxes(appsCollection, reviewsCollection)

    apps = appsCollection.find({})

    for app in apps:
        reviews = reviewsCollection.find_one({'appId': ObjectId(app['_id'])})
        (rating, launchDayOffset, reviewCount, frequencies) = getAppVariableData(app, reviews)
        
        if reviewCount != 0:
            print("rating:", rating)
            print("days offset:", launchDayOffset)
            print("review count:", reviewCount)
            print("")
