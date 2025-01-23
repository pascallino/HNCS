import json
import operator
from django.http import JsonResponse
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
                # Create a Story
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
            
            if  type == 'job':
                # Create a job
                job = Job(
                    job_id=random.randint(80000000, 9000000000),
                    by=validated_data.get('by'),
                    score=0,
                    deleted=False,
                    text=validated_data.get('text', ''),
                    title=validated_data.get('title', ''),
                    type=validated_data.get('type', ''),
                    url=validated_data.get('url', ''),
                    time=validated_data['time'],
                    dead=False,
                    in_house= 'Yes',
                    
                )
                job.save()
                return Response({"message": "job created successfully", "id": job.job_id}, status=status.HTTP_201_CREATED)
        
            if  type == 'poll':
                # Create a Story
                poll = Poll(
                    poll_id=random.randint(80000000, 9000000000),
                    by=validated_data.get('by'),
                    descendants=0,
                    kids=[],
                    parts=[],
                    score=0,
                    deleted=False,
                    text=validated_data.get('text', ''),
                    title=validated_data.get('title', ''),
                    type=validated_data.get('type', ''),
                    time=validated_data['time'],
                    dead=False,
                    in_house= 'Yes',
                    
                )
                poll.save()
                return Response({"message": "poll created successfully", "id": poll.poll_id}, status=status.HTTP_201_CREATED)

                
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def index(request):
    type_value = ''
    syncval = SyncVal.objects.first()
    if not syncval:
        syncval = SyncVal(value=0)
        syncval.save()
     # Fetch data from API
    # timezone_ = request.session['timezone']  # Store in session
    # if timezone_:
    #     activate(timezone_)
    type = request.GET.get('type', '')
    print(type)
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
        type_value = type
        items = [
            item for item in items
            if search_query in (item.get('title') or '').lower() or  search_query in (item.get('text') or '').lower()
        ]
    if items:
        type_value = items[0]['type']

    # Paginate data
    paginator = Paginator(items, 4)  # 4 cards per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj, 'type': type_value})


def details(request, item_id, type):
    item_url = f"https://hacker-news.firebaseio.com/v0/item/{item_id}.json?print=pretty"
    item_response = requests.get(item_url)
    item_data = item_response.json() if item_response.status_code == 200 else {}
    if not item_data:
        if type == 'story':
            item_data = Story.objects.filter(story_id=item_id).first()
        elif type == 'job':
            item_data = Job.objects.filter(job_id=item_id).first()
        else:
            item_data = Poll.objects.filter(poll_id=item_id).first()
    return render(request, 'details.html', {'story': item_data, 'item_id': item_id})


def create_get(request):
     return render(request, 'create.html', {'create_link': 1})
 
 
def delete_item(request, itemId, type):
    if type == 'story':
        story = Story.objects.filter(story_id=itemId).first()
        if story:
            story.delete()
            return JsonResponse({'status': 'success'})
    if type == 'job':
        job = Job.objects.filter(job_id=itemId).first()
        if job:
            job.delete()
            return JsonResponse({'status': 'success'})
    if type == 'poll':
        poll = Poll.objects.filter(poll_id=itemId).first()
        if poll:
            poll.delete()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def get_item(request, itemId, type):
    if type == 'story':
        story = Story.objects.filter(story_id=itemId).first()
        if story:
            # Return story data as JSON
            return JsonResponse({
                'story_id': story.story_id,
                'by': story.by,
                'title': story.title,
                'url': story.url,
                'type': story.type,
                'id': story.story_id
                
            })
        else:
            return JsonResponse({'error': 'Story not found'}, status=404)
    
    if type == 'job':
        job = Job.objects.filter(job_id=itemId).first()
        if job:
            # Return story data as JSON
            return JsonResponse({
                'job_id': job.job_id,
                'by': job.by,
                'title': job.title,
                'text': job.text,
                'url': job.url,
                'type': job.type,
                'id': job.job_id
                
            })
        else:
            return JsonResponse({'error': 'job not found'}, status=404)
    if type == 'poll':
        poll = Poll.objects.filter(poll_id=itemId).first()
        if poll:
            # Return story data as JSON
            return JsonResponse({
                'poll_id': poll.poll_id,
                'by': poll.by,
                'title': poll.title,
                'text': poll.text,
                'type': poll.type,
                'id': poll.poll_id
                
            })
        else:
            return JsonResponse({'error': 'Poll not found'}, status=404)

    return JsonResponse({'error': 'Invalid type'}, status=400)



def modify_item(request, itemId, type):
    data = json.loads(request.body)
    if type == 'story':
        story = Story.objects.filter(story_id=itemId).first()
        if story:
            story.by = data.get('by')
            story.title = data.get('title')
            story.url =  data.get('url', '')
            story.save()
            return JsonResponse({'status': 'success'})
    if type == 'job':
        job = Job.objects.filter(job_id=itemId).first()
        if job:
            job.by = data.get('by')
            job.title = data.get('title')
            job.text = data.get('text')
            job.url =  data.get('url', '')
            job.save()
            return JsonResponse({'status': 'success'})
    if type == 'poll':
        poll = Poll.objects.filter(poll_id=itemId).first()
        if poll:
            poll.by = data.get('by')
            poll.title = data.get('title')
            poll.text = data.get('text')
            poll.url =  data.get('url', '')
            poll.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})
     
     
     
   


