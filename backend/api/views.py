from rest_framework.response import Response
from rest_framework.decorators import api_view
from tinydb import TinyDB, Query
import os

DB_FILE = os.path.join("data", "shopify_apps.json")
db = TinyDB(DB_FILE)

App = Query()

@api_view(['GET'])
def getData(request):
    return Response("data")

@api_view(['GET'])
def getTest(request):
    apps = db.search(App.reviewCount == 100)
    return Response(apps)

@api_view(['GET'])
def getTest2(request):
    app = db.get(Query()['url'] == 'https://apps.shopify.com/pushup-notification-marketing')
    return Response(app)

@api_view(['GET'])
def getUrls(request):
    apps = db.all()
    urls = []
    for _app in apps:
        urls.append(_app['url'])
    return Response(urls)