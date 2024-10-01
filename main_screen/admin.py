from django.contrib import admin
from .models import Group, Order

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_fac', 'group_kaf', 'group_course', 'group_count', 'contact', 'contact_phone')
    search_fields = ('group_fac', 'group_kaf', 'group_course', 'contact')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'group', 'date', 'audience', 'teacher')
    list_filter = ('date', 'group')
    search_fields = ('audience', 'teacher')

    def save_model(self, request, obj, form, change):
        try:
            obj.clean()  # Проверка уникальности перед сохранением
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            form.add_error(None, e)
