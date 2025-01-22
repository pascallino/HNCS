from django.db import models
# Create your models here.
from mongoengine import EmbeddedDocument,  Document, StringField, DateTimeField, IntField, BooleanField, ReferenceField, ListField, EmbeddedDocumentListField, CASCADE

import datetime

class Comment(Document):
    comment_id = IntField(required=True)  # Changed to IntField to match the data
    by = StringField()  # The username of the item's author
    kids = ListField(IntField())  # Child comment IDs (if storing as integers)
    parent = IntField()  # Parent comment ID
    deleted = BooleanField(default=False)
    text = StringField()
    time = DateTimeField()  # Ensure Unix time is converted to datetime when saving
    type = StringField(choices=["job", "story", "comment", "poll", "pollopt"])  # Limited to valid types
    dead = BooleanField(default=False)


class Story(Document):
    story_id = IntField(required=True)  # Changed to IntField to match the data
    by = StringField()  # The username of the item's author
    descendants = IntField()
    kids = ListField(IntField())  # Stores a list of integers
    score = IntField()
    deleted = BooleanField(default=False)
    title = StringField()
    type = StringField(choices=["job", "story", "comment", "poll", "pollopt"])  # Limited to valid types
    url = StringField()  # URL of the story
    time = DateTimeField()  # Ensure Unix time is converted to datetime when saving
    dead = BooleanField(default=False)
    in_house = StringField(default="No") 
    
class Job(Document):
    by = StringField()  # The username of the item's author
    job_id = IntField(required=True)  # Changed to IntField to match the data
    score = IntField()
    deleted = BooleanField(default=False)
    text = StringField()
    time = DateTimeField()  # Ensure Unix time is converted to datetime when saving
    title = StringField()
    type = StringField(choices=["job", "story", "comment", "poll", "pollopt"])  # Limited to valid types
    url = StringField()  # URL of the story
    dead = BooleanField(default=False)
    in_house = StringField(default="No") 

class Poll(Document):
    by = StringField()  # The username of the item's author
    decendants = IntField() #decendants total comment counts
    poll_id = IntField(required=True)  # Changed to IntField to match the data
    kids = ListField(IntField()) 
    parts = ListField(IntField()) 
    score = IntField()
    deleted = BooleanField(default=False)
    text = StringField()
    time = DateTimeField()  # Ensure Unix time is converted to datetime when saving
    title = StringField()
    type = StringField(choices=["job", "story", "comment", "poll", "pollopt"])  # Limited to valid types
    dead = BooleanField(default=False)
    in_house = StringField(default="No") 
    
class Pollopt(Document):
    by = StringField()
    pollopt_id = IntField()
    poll = IntField()
    score = IntField()
    text = StringField()
    time = DateTimeField()
    type = StringField(choices=["job", "story", "comment", "poll", "pollopt"])  # Limited to valid types

class SyncVal(Document):
    value = IntField()