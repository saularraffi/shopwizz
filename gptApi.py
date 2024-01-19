import requests
import openai
import os
from dotenv import load_dotenv
import json
from tinydb import TinyDB, Query

DB_FILE = "shopify_apps.json"
db = TinyDB(DB_FILE)


load_dotenv()

openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")

# reviews = [
#     "I have been using the free version for a long time. Then I decided to upgrade my plan and it was a disaster. Faced so many issues within the app, tried to contact support but either they are very busy or just lame. My issues are still pending. Templates are approved on Facebook but they are pending in apps.",
#     "Worst support ever. We had a big issue migrating a store. An automation was trigger and sent messages to clients of all orders. We asked for support and never received any help. This app should be unlisted from Shopify.",
#     "The support team is the worst. Didn't like the service. Poor user interface very difficult non supportive staff",
#     "dont use this app , they charge you money without working ! no customer support no answer since 5 days ! and they have take the money! very poor !"
# ]

def getTestReviews():
    App = Query()
    app = db.search(App.url == 'https://apps.shopify.com/subliminator')
    reviewObj = app[0]['reviews']

    reviews = []

    for star, _ in reviewObj.items():
        if star == "1-star" or star == "2-star":
            for review in reviewObj[star]['content']:
                if len(review) < 1000: reviews.append(review)
    
    return reviews

def askGpt(systemPrompt, userPrompt):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer ' + openai.api_key,
    }

    jsonData = {
        'model': 'gpt-4',
        'messages': [
            { 'role': 'system', 'content': systemPrompt },
            { 'role': 'user', 'content': userPrompt },
        ],
        'temperature': 0.7,
    }

    response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=jsonData)

    return response.json()['choices'][0]['message']['content']

def buildUserPrompt(reviews):
    promptIntro = "Here are the reviews: "
    reviewsString = ""

    for review in reviews:
        reviewsString += "\"\"\"" + review + "\"\"\", "

    return promptIntro + reviewsString

systemPrompt = """
You are provided with a list of reviews for a Shopify app.  Reviews are each wrapped in triple quotation marks and delimited by a comma.  Analyze each review and provide a response, in JSON format, containing the top 3 problems users have with the app. The JSON response should have the following structure:

{
    "problems": [
        {
            "overview": String,
            "severity": Number,
            "details": List<String>
        }
    ]
}

Here is the purpose of each JSON field:

overview: A description of the problem.
severity: A numerical score between 0 and 100 that denotes how frequent users complain about this problem.
details: A list of additional details regarding this problem. Be specific and do not directly quote from the reviews. Provide numerical values when possible.
"""

reviews = getTestReviews()
userPrompt = buildUserPrompt(reviews)
response = askGpt(systemPrompt, userPrompt)
appReviewsAnalysis = json.loads(response) 

for problem in appReviewsAnalysis['problems']:
    print("Problem Overview: ", problem['overview'])
    print("Severity Score  : ", problem['severity'])
    print("Details: ")
    for detail in problem['details']:
        print("\t*", detail)
    print("")