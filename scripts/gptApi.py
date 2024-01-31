from dotenv import load_dotenv
import requests
import openai
import random
import json
import math
import os

# GPT ERROR MESSAGE EXAMPLE
# {
#   "error": {
#     "message": "Rate limit reached for gpt-4 in organization org-flTcFblz5jti29nTLQcuDors on tokens per min (TPM): Limit 10000, Used 3403, Requested 9031. Please try again in 14.604s. Visit https://platform.openai.com/account/rate-limits to learn more.",
#     "type": "tokens",
#     "param": "None",
#     "code": "rate_limit_exceeded"
#   }
# }

load_dotenv()
openai.organization = os.getenv("OPENAI_ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")

GPT_ENDPOINT = 'https://api.openai.com/v1/chat/completions'
GPT_4_MODEL = 'gpt-4'
GPT_4_TURBO_MODEL = 'gpt-4-1106-preview'
GPT_3_TURBO_MODEL = 'gpt-3.5-turbo-1106'

SYSTEM_PROMPT2 = """
You are provided with a list of reviews for a Shopify app.  Reviews are each wrapped in triple quotation marks and delimited by a comma.  Analyze each review and provide a response, in JSON format, containing the top 3 problems users have with the app. The JSON response should have the following structure:

{
    "problems": [
        {
            "overview": String,
            "severity": Number,
            "frequency": Number,
            "details": List<String>
        }
    ]
}

Here is the purpose of each JSON field:

overview: A description of the problem.
severity: A numerical score between 0 and 100 that reflects how sever this problem is to users.
frequency: The frequency of the problem being mention. Calculate this by taking the number of review that mention this problem and dividing by the total number of reviews.
details: A list of additional details regarding this problem. Be specific and do not directly quote from the reviews. Provide numerical values when possible.
"""

SYSTEM_PROMPT = """You are provided with a list of reviews for a Shopify app.  
Reviews are each wrapped in triple quotation marks and delimited by a comma.  
Analyze each review and provide the top 3 problems users have with the app.
Your response should be a JSON object called "problems" containing a list of 3 elements.

The first column, called "overview", should describe the problem.

The second column, called "severity", should be a numerical score between 0 and 100 that reflects how sever this problem is to users.

The third column, called "frequency", should represent the frequency of the problem being mention.
Calculate the "frequency" column by taking the number of review that mention this problem and dividing by the total number of reviews.

The forth column, called "details", should be a list of between 3 and 5 items that specify additional details regarding this problem.

Problems in the "problems" field should be ordered by the frequency and severity of the problem.
"""

# DRAFT FUNCTION: Eventually take review sets that are too large and split the requests up to gpt
def getReviewSampleSet(reviews, tokenCount):
    numberOfBatches = math.ceil(tokenCount/9000)
    batches = [[] for _ in range(numberOfBatches)]
    indicies = []

    for i in range(0, len(reviews)):
        indicies.append(i)

    random.shuffle(indicies)

    while len(indicies) > 0:
        for i in range(len(batches)):
            if len(indicies) == 0:
                break
            index = indicies.pop()
            if len(reviews[index]) > 800:
                batches[i].append(reviews[index])

    return batches

def countTokens(reviews):
    chars = 0
    for review in reviews:
        chars += len(review)
    return math.floor(chars/4)

class GptReviewAnalyzer:
    def __init__(self, reviews, tokenLimit=8000):
        self.reviews = sorted(reviews, key=len)
        self.tokenLimit = tokenLimit
        self.userPrompt = self.buildUserPrompt()

    def run(self):
        response = openai.ChatCompletion.create(
            model=GPT_4_TURBO_MODEL,
            messages=[
                { 'role': 'system', 'content': SYSTEM_PROMPT },
                { 'role': 'user', 'content': self.userPrompt }
            ],
            response_format={ "type": "json_object" },
            temperature=0
        )

        if "error" in response:
            return response
                
        responseContent = response['choices'][0]['message']['content']
        return json.loads(responseContent)    

    def runViaHttpRequest(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + openai.api_key,
        }

        jsonData = {
            'model': GPT_4_MODEL,
            'messages': [
                { 'role': 'system', 'content': SYSTEM_PROMPT },
                { 'role': 'user', 'content': self.userPrompt },
            ],
            'temperature': 0.7,
        }

        response = requests.post(GPT_ENDPOINT, headers=headers, json=jsonData)
        responseJson = response.json()

        if "error" in responseJson:
            return responseJson
                
        responseContent = responseJson['choices'][0]['message']['content']
        return json.loads(responseContent)
    
    def enforceTokenCompliance(self):
        while countTokens(self.reviews) > self.tokenLimit:
            self.reviews.pop()

    def buildUserPrompt(self):
        self.enforceTokenCompliance()

        promptIntro = "Here are the reviews: "
        reviewsString = ""

        for review in self.reviews:
            reviewsString += "\"\"\"" + review + "\"\"\", "

        return promptIntro + reviewsString
