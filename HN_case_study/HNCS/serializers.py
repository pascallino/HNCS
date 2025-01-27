from rest_framework import serializers
from .models import Story


class GenericItemSerializer(serializers.Serializer):
    story_id = serializers.IntegerField(required=False)
    job_id = serializers.IntegerField(required=False)
    poll_id = serializers.IntegerField(required=False)
    by = serializers.CharField(required=False)
    descendants = serializers.IntegerField(required=False)
    poll = serializers.IntegerField(required=False)
    parent = serializers.IntegerField(required=False)
    kids = serializers.ListField(child=serializers.IntegerField(), required=False)
    parts = serializers.ListField(child=serializers.IntegerField(), required=False)
    score = serializers.IntegerField(required=False)
    deleted = serializers.BooleanField(default=False)
    text = serializers.CharField(required=False)
    title = serializers.CharField(required=False)
    type = serializers.CharField(required=False)
    url = serializers.CharField(required=False)
    time = serializers.DateTimeField()
    dead = serializers.BooleanField(default=False)
    in_house = serializers.CharField(required=False) 