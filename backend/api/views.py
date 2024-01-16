from rest_framework.response import Response
from rest_framework.decorators import api_view
from tinydb import TinyDB, Query
import os

DB_FILE = os.path.join("data", "shopify_apps.json")
db = TinyDB(DB_FILE)

@api_view(['GET'])
def getData(request):
    app = db.get(Query()['url'] == 'https://apps.shopify.com/pushup-notification-marketing')
    return Response(app)