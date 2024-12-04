from django.contrib import admin
from django import forms
from .models import Group, Lesson, LessonGroup

class LessonGroupForm(forms.ModelForm):
    class Meta:
        model = LessonGroup
        fields = ['lesson', 'group', 'building', 'audience', 'headboy']

    def clean(self):
        cleaned_data = super().clean()
        lesson = cleaned_data.get('lesson')


class LessonGroupInline(admin.TabularInline):
    model = LessonGroup
    form = LessonGroupForm
    extra = 1

class LessonAdmin(admin.ModelAdmin):
    inlines = [LessonGroupInline]
    list_display = ('id', 'name', 'date', 'time', 'status')
    list_filter = ('status',)
    search_fields = ('name',)

class GroupAdmin(admin.ModelAdmin):
    list_display = ('facultet', 'kafedra', 'course', 'count', 'headboy', 'status')
    list_filter = ('status',)
    search_fields = ('facultet', 'kafedra', 'headboy')

class LessonGroupAdmin(admin.ModelAdmin):
    list_display = ('lesson', 'group', 'building', 'audience', 'headboy')
    list_filter = ('lesson', 'group')

admin.site.register(Lesson, LessonAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(LessonGroup, LessonGroupAdmin)
