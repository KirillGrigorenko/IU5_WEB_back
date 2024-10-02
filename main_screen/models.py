from django.db import models
from datetime import datetime

class Group(models.Model):
    group_fac = models.CharField(max_length=100)
    group_kaf = models.CharField(max_length=100)
    group_course = models.PositiveIntegerField()
    group_count = models.PositiveIntegerField()
    contact = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    photo_url = models.CharField(max_length=254, default='')
    status = models.CharField(max_length=10, default='Действует')

    def __str__(self):
        return f'{self.group_fac.replace(" ", "")}{self.group_kaf.replace(" ", "")}-{self.group_course}{self.group_count}'


class Order(models.Model):
    groups = models.ManyToManyField(Group, through='OrderGroup')
    building = models.CharField(max_length=30, default='ГЗ')
    status = models.CharField(max_length=10, default='черновик')

    def __str__(self):
        return f"Order for {', '.join([str(group).replace(' ', '') for group in self.groups.all()])}"


class OrderGroup(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    lesson_time = models.DateTimeField()
    audience = models.CharField(max_length=100)

    class Meta:
        unique_together = ['order', 'group']

    def __str__(self):
        return f'Order {self.order.id} - Group {self.group.id} ({self.audience})'
