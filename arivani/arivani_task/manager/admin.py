from django.contrib import admin
from manager.models import *
# Register your models here.
@admin.register(ManagerModel)
class ManagerModelAdmin(admin.ModelAdmin):
    list_display=('managerID','name','is_deleted','status',
    'created_by','updated_by','created_at','updated_at','deleted_by','deleted_at','restored_at','restored_by')
    list_display_links=('name',)