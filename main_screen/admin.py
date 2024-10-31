from django.contrib import admin
from .models import Group, Lesson, LessonGroup


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('facultet', 'kafedra', 'course', 'count', 'headboy', 'contact_phone', 'photo_url', 'status')
    search_fields = ('facultet', 'kafedra', 'course', 'headboy')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'time', 'date', 'status', 'display_groups')
    search_fields = ('time', 'date') 

    def display_groups(self, obj):
        return ', '.join([str(group).replace(' ', '') for group in obj.groups.all()])
    display_groups.short_description = 'Groups'

@admin.register(LessonGroup)
class LessonGroupAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'group', 'building', 'audience', 'headboy')
    search_fields = ('lesson', 'group', 'building', 'audience', 'headboy')
