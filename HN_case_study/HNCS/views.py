from django.shortcuts import render
import datetime
from .models import *
import requests
# Create your views here.

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.decorators import login_required
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from .models import Story, Poll, Job  # MongoDB models
from .serializers import GenericItemSerializer
from django.core.paginator import Paginator

class ItemAPIView(APIView):
    renderer_classes = [JSONRenderer]
    def get(self, request, type=None):
        # Filter by type (story, poll, job)
        if type == "story":
            items = Story.objects.all()
        elif type == "poll":
            items = Poll.objects.all()
        elif type == "job":
            items = Job.objects.all()
        else:
            return Response({"error": "Invalid type"}, status=400)

        serializer = GenericItemSerializer(items, many=True)
        return Response(serializer.data)


def index(request):
    syncval = SyncVal.objects.first()
    if not syncval:
        syncval = SyncVal(value=0)
        syncval.save()
     # Fetch data from API
    type = request.GET.get('type', '')
    if type == 'story':
        response = requests.get("http://localhost:8000/api/item/story")
    elif type ==  'job':
         response = requests.get("http://localhost:8000/api/item/job")
    elif type == 'poll':
         response = requests.get("http://localhost:8000/api/item/poll")
    else:
        response = requests.get("http://localhost:8000/api/item/story")
        
    if response.status_code == 200:
        items = response.json()
    else:
        items = []
    
    search_query = request.GET.get('q', '').lower()  # Get the search term from the query parameters
    if search_query:
        items = [
            item for item in items
            if search_query in (item.get('title') or '').lower() or  search_query in (item.get('text') or '').lower()
        ]


    # Paginate data
    paginator = Paginator(items, 4)  # 4 cards per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, 'index.html', {'page_obj': page_obj})


def details(request, item_id):
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{126809}.json?print=pretty"
    item_response = requests.get(item_url)
    item_data = item_response.json() if item_response.status_code == 200 else {}
    return render(request, 'details.html', {'story': item_data, 'item_id': item_id})
   


