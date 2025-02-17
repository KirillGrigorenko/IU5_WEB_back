from .models import Group,Lesson, LessonGroup
from django.contrib.auth.models import User
from rest_framework import serializers


class AllGroupsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "facultet", "kafedra", "course", "count", "headboy", "contact_phone", "photo_url"]
        read_only_fields = ["id"]
