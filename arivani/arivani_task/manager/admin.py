from django.contrib import admin
from manager.models import *
# Register your models here.
@admin.register(ManagerModel)
class ManagerModelAdmin(admin.ModelAdmin):
    list_display=('managerID','name','is_deleted','status', 'hr_under_manager_list',
    'created_by','updated_by','created_at','updated_at','deleted_by','deleted_at','restored_at','restored_by')
    list_display_links=('name',)

    def hr_under_manager_list(self,objects):
        return [object.name for object in objects.hr_under_manager.all()]              
        