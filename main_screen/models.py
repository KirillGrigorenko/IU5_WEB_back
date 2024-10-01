from django.db import models
from django.core.exceptions import ValidationError

class Group(models.Model):
    group_fac = models.CharField(max_length=100)
    group_kaf = models.CharField(max_length=100)
    group_course = models.PositiveIntegerField()
    group_count = models.PositiveIntegerField()
    contact = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)

    def __str__(self):
        return self.group_fac
        
    def save(self, *args, **kwargs):
        if self.group_count > 50:
            raise ValidationError("Group count cannot exceed 50.")
        super().save(*args, **kwargs)

class Order(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField()
    audience = models.CharField(max_length=100)
    teacher = models.CharField(max_length=100)

    def __str__(self):
        return f"Order for {self.group} on {self.date}"

    def save(self, *args, **kwargs):
        if Order.objects.filter(group=self.group, date=self.date).exists():
            raise ValidationError("An order for this group on this date already exists.")
        super().save(*args, **kwargs)
