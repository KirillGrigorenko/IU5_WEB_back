from rest_framework import serializers
from .models import Group, Lesson, LessonGroup
from django.contrib.auth.models import User

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "facultet", "kafedra", "course", "count", "headboy", "contact_phone", "photo_url", "status", "is_active"]
        read_only_fields = ["id"]

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            "id",
            "name",
            "status",
            "creation_datetime",
            "formation_datetime",
            "completion_datetime",
            "lecturer",  
            "manager",   
            "time",
            "date",
            "building",
            "audience"
        ]
        read_only_fields = ["id"]


class LessonGroupSerializer(serializers.ModelSerializer):

    group = GroupSerializer(read_only=True)

    class Meta:
        model = LessonGroup
        fields = ["lesson", "group", "headboy"]

class LessonFilterSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Lesson.LessonStatus.choices, required=False)
    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)

    def filter_lessons(self, queryset):
        """
        Фильтрация заявок по статусу и диапазону дат
        """
        status = self.validated_data.get('status')
        start_date = self.validated_data.get('start_date')
        end_date = self.validated_data.get('end_date')

        if status:
            queryset = queryset.filter(status=status)
        if start_date:
            queryset = queryset.filter(formation_datetime__gte=start_date)
        if end_date:
            queryset = queryset.filter(formation_datetime__lte=end_date)
        
        return queryset

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),  # Если email нет, просто None
            password=validated_data['password']
        )
        return user

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        if 'password' in validated_data and validated_data['password']:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
