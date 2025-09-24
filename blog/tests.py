import requests
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_random_quote(request):
    response = requests.get("https://api.quotable.io/random")
    data = response.json()
    return Response({
        "quote": data.get("content"),
        "author": data.get("author")
    })
