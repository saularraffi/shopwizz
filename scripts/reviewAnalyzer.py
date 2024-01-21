from gptApi import GptReviewAnalyzer
from tinydb import TinyDB, Query
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))
DB_FILE = os.path.join(SCRIPT_PATH, "..", "shopify_apps.json")
db = TinyDB(DB_FILE)

App = Query()
# url = 'https://apps.shopify.com/subliminator'
url = 'https://apps.shopify.com/klaviyo-email-marketing'
app = db.search(App.url == url)
reviewObj = app[0]['reviews']

reviews = []

for star, _ in reviewObj.items():
    if star == "1-star" or star == "2-star":
        for review in reviewObj[star]['content']:
            if len(review) < 1000: reviews.append(review)

reviewAnalyzer = GptReviewAnalyzer(reviews)
response = reviewAnalyzer.run()

if "error" in response:
    print("ERROR:", response["error"]["message"])
    exit(0)

for problem in response['problems']:
    print("Problem Overview: ", problem['overview'])
    print("Severity Score  : ", problem['severity'])
    print("Details: ")
    for detail in problem['details']:
        print("\t*", detail)
    print("")