from django.contrib import admin
from .models import Group, Order, OrderGroup

class OrderGroupInline(admin.TabularInline):
    model = OrderGroup
    extra = 1
    fields = ('group', 'lesson_time', 'audience')

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_fac', 'group_kaf', 'group_course', 'group_count', 'contact', 'contact_phone', 'photo_url', 'status')
    search_fields = ('group_fac', 'group_kaf', 'group_course', 'contact')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'building', 'status', 'display_groups')
    search_fields = ('building',)
    inlines = [OrderGroupInline]

    def display_groups(self, obj):
        return ', '.join([str(group).replace(' ', '') for group in obj.groups.all()])
    display_groups.short_description = 'Groups'

@admin.register(OrderGroup)
class OrderGroupAdmin(admin.ModelAdmin):
    list_display = ('order', 'group', 'lesson_time', 'audience')
    search_fields = ('order__id', 'group__group_fac', 'lesson_time', 'audience')
