from datetime import datetime

def normalize(x, xMin, xMax, multiplier):
    return round(((x - xMin) / (xMax - xMin)) * multiplier, 1)

def getDaysOffset(dateString):
    try:
        date = datetime.strptime(dateString, '%m-%d-%Y').date()
        today = datetime.today().date()
        offset = today - date
        return offset.days
    except Exception as e:
        return -1