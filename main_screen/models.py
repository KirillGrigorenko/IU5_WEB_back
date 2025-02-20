from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils import timezone

class Group(models.Model):
    facultet = models.CharField(max_length=100)
    kafedra = models.CharField(max_length=100)
    course = models.PositiveIntegerField()
    count = models.PositiveIntegerField()
    headboy = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    photo_url = models.CharField(max_length=254, null=False ,default="")
    status = models.CharField(max_length=10, default='Действует')
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f'{self.facultet.replace(" ", "")}{self.kafedra.replace(" ", "")}-{self.course}{self.count}'

class Lesson(models.Model):
    class LessonStatus(models.TextChoices):
        DRAFT = "Черновик"
        DELETED = "Удалён"
        FORMED = "Сформирован"
        COMPLETED = "Завершён"
        REJECTED = "Отклонён"

    status = models.CharField(max_length=30, choices=LessonStatus.choices, default=LessonStatus.DRAFT)
    creation_datetime = models.DateTimeField(auto_now_add=True)
    formation_datetime = models.DateTimeField(blank=True, null=True)
    completion_datetime = models.DateTimeField(blank=True, null=True)
    lecturer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_requests')
    manager = models.ForeignKey(User, on_delete=models.CASCADE, related_name='managed_requests',blank=True, null=True)
    name = models.CharField(max_length=100, default='РИП')
    time = models.CharField(max_length=30, default='12:00')
    date = models.DateField(default=timezone.now)
    building = models.CharField(max_length=100, default='ГЗ')
    audience = models.CharField(max_length=100, default='209')
    
    def __str__(self):
        return f"Lesson {self.name} on {self.date} at {self.time} in {self.building}  audience {self.audience}"

    class Meta:
        db_table = 'lessons'

class LessonGroup(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    headboy = models.CharField(max_length=100)

    class Meta:
        db_table = 'Lesson_in_progress'
        unique_together = ('lesson', 'group')

    def __str__(self):
        return f'Lesson {self.lesson.id} - Group {self.group.id}'