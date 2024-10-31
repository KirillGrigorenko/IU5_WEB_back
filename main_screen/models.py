from django.db import models
from datetime import datetime

class Group(models.Model):
    facultet = models.CharField(max_length=100)
    kafedra = models.CharField(max_length=100)
    course = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    headboy = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    photo_url = models.CharField(max_length=254, default='')
    status = models.CharField(max_length=10, default='Действует')

    def __str__(self):
        return f'{self.facultet.replace(" ", "")}{self.kafedra.replace(" ", "")}-{self.course}{self.count}'


class Lesson(models.Model):
    groups = models.ManyToManyField(Group, through='LessonGroup')
    time = models.CharField(max_length=30, default='ГЗ')
    date = models.DateField(default=datetime.now)
    status = models.CharField(max_length=10, default='черновик')

    def __str__(self):
        return f"Lesson for {', '.join([str(group).replace(' ', '') for group in self.groups.all()])}"


class LessonGroup(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    building = models.CharField(max_length=100)
    audience = models.CharField(max_length=100)
    headboy = models.CharField(max_length=100)

    class Meta:
        unique_together = ['lesson', 'group']

    def __str__(self):
        return f'Lesson {self.lesson.id} - Group {self.group.id} ({self.audience})'


