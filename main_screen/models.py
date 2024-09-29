from django.db import models

from django.template.defaultfilters import register
from django.utils import timezone 

@register.filter
def multiply_minus_one(value):
    """Умножает значение на два и вычитает единицу."""
    return int(value) * 2 - 1
