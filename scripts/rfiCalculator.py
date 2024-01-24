from util import normalize, getDaysOffset
from math import floor

WEIGHTS = {
    "rating": 8,
    "daysActive": 2,
    "reviewCount": 5,
    "problemsFrequency": 7,
    "freq1": 5,
    "freq2": 3,
    "freq3": 2,
}

class RfiCalculator():
    daysActiveMinMax = ()
    reviewCountsMinMax = ()

    def __init__(self, appObj):
        self.app = appObj
        self.rating = -1
        self.rfiScore = -1
        self.problemsFrequencies = []
        self.normalizedDaysActive = -1
        self.normalizedReviewCount = -1
        
    def getScore(self):
        if RfiCalculator.daysActiveMinMax == () or RfiCalculator.reviewCountsMinMax == ():
            print("Cannot calculate RFI score before setting min/max data")
            return -1
        else:
            self.setAppVariableData()
            self.calculateRfiScore()
            return self.rfiScore
    
    def calculateRfiScore(self):
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
        
        a = WEIGHTS['reviewCount']
        b = WEIGHTS['rating']
        c = WEIGHTS['problemsFrequency']
        d = WEIGHTS['daysActive']
        c1 = WEIGHTS['freq1']
        c2 = WEIGHTS['freq2']
        c3 = WEIGHTS['freq3']

        frequencyScore = c1*self.problemsFrequencies[0] + c2*self.problemsFrequencies[1] + c3*self.problemsFrequencies[2]        
        self.rfiScore = floor((a*self.normalizedReviewCount / b*self.rating) + c*frequencyScore + d*self.normalizedDaysActive)
        
        # print("review count:", reviewCount, a*reviewCount)
        # print("rating:", rating, b*rating)
        # print("frequency:", frequencyScore, c*frequencyScore)
        # print("launch day offset:", daysActive, d*daysActive)
        # print("RFI Score:", rfiScore, "\n")
    
    def setAppVariableData(self):
        offset = getDaysOffset(self.app['dateLaunched'])
        daysActive = offset if offset != -1 else 0
        normalizedDaysActive = normalize(
            daysActive,
            RfiCalculator.daysActiveMinMax[0],
            RfiCalculator.daysActiveMinMax[1],
            100
        )

        reviewCount = self.app['reviewCount'] if self.app['reviewCount'] is not None else 0
        normalizedReviewCount = normalize(
            reviewCount,
            RfiCalculator.reviewCountsMinMax[0],
            RfiCalculator.reviewCountsMinMax[1],
            1000
        )
        
        self.problemsFrequencies = [0, 0, 0]
        self.normalizedDaysActive = normalizedDaysActive
        self.normalizedReviewCount = normalizedReviewCount
        self.rating = self.app['rating'] if self.app['rating'] is not None else 0