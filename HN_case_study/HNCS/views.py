import operator
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
from rest_framework import status
import random
import uuid
from django.utils.timezone import activate


def generate_unique_id():
    return uuid.uuid4().int & (1 << 64) - 1  

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


class CreateItemAPIView(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request, type):
        # timezone_ = request.data.get('timezone')
        # if timezone_:
        #     request.session['timezone'] = timezone_  # Store in session
        #     activate(timezone_)
        serializer = GenericItemSerializer(data=request.data)
        if serializer.is_valid():
            # Process the validated data
            validated_data = serializer.validated_data
            
            if  type == 'story':
                print('story')
                # Create a Story instance if needed
                story = Story(
                    story_id=random.randint(80000000, 9000000000),
                    by=validated_data.get('by'),
                    descendants=0,
                    kids=[],
                    score=0,
                    deleted=False,
                    title=validated_data.get('title', ''),
                    type=validated_data.get('type', ''),
                    url=validated_data.get('url', ''),
                    time=validated_data['time'],
                    dead=False,
                    in_house= 'Yes',
                    
                )
                story.save()
            
            return Response({"message": "story created successfully", "id": story.story_id}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def index(request):
    syncval = SyncVal.objects.first()
    if not syncval:
        syncval = SyncVal(value=0)
        syncval.save()
     # Fetch data from API
    # timezone_ = request.session['timezone']  # Store in session
    # if timezone_:
    #     activate(timezone_)
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
        items = sorted(response.json(), key=operator.itemgetter('time'), reverse=True)
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


def details(request, item_id, type):
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json?print=pretty"
    item_response = requests.get(item_url)
    item_data = item_response.json() if item_response.status_code == 200 else {}
    if not item_data:
        if type == 'story':
            item_data = Story.objects.filter(story_id=item_id).first()
    return render(request, 'details.html', {'story': item_data, 'item_id': item_id})


def create_get(request):
     return render(request, 'create.html', {'create_link': 1})
   


